"""DICOM reading context."""

import dataclasses
import logging
import typing as t
import warnings
from contextlib import contextmanager

import pydicom.config as pydicom_config
from fw_utils.datetime import get_datetime
from pydicom.datadict import dictionary_VR
from pydicom.dataelem import DataElement, RawDataElement
from pydicom.dataset import Dataset
from pydicom.filebase import DicomBytesIO
from pydicom.filewriter import write_data_element
from pydicom.hooks import hooks
from pydicom.sequence import Sequence
from pydicom.tag import BaseTag, Tag
from pydicom.values import convert_value, validate_value

from .. import NAME
from .config import get_config
from .validation import get_required_tags, get_standard

log = logging.getLogger(__name__)

OAS: str = "OriginalAttributesSequence"
NAS: str = "NonconformingModifiedAttributesSequence"
MAS: str = "ModifiedAttributesSequence"

READER: str = "ReadContext"


@contextmanager
def no_fixes():
    """Context manager that empties callbacks/fixers."""
    config = get_config()
    orig_VR_fixers = config.raw_VR_fixers
    orig_value_fixers = config.raw_value_fixers
    config.raw_VR_fixers = []
    config.raw_value_fixers = []
    orig_wrong_len = pydicom_config.convert_wrong_length_to_UN
    orig_vr_from_un = pydicom_config.replace_un_with_known_vr
    # NOTE: Ensure there is no VR inference or fixes applied
    # when testing if a DataElement can be written as is.
    pydicom_config.replace_un_with_known_vr = False
    pydicom_config.convert_wrong_length_to_UN = False
    try:
        yield
    finally:
        config.raw_VR_fixers = orig_VR_fixers
        config.raw_value_fixers = orig_value_fixers
        pydicom_config.replace_un_with_known_vr = orig_vr_from_un
        pydicom_config.convert_wrong_length_to_UN = orig_wrong_len


@dataclasses.dataclass
class ReplaceEvent:
    """Dataclass to hold tracking event information."""

    field: str
    old: t.Optional[str]
    new: str

    def __repr__(self):
        """Return representation of tracking event."""
        return f"Replace {self.field}: {self.old} -> {self.new}"


class TrackedRawDataElement(RawDataElement):
    """RawDataElement subclass adding change tracking to _replace events."""

    id_: int
    original: RawDataElement
    events: t.List[ReplaceEvent]

    def __new__(cls, *args, id_=None, **kwargs) -> "TrackedRawDataElement":
        """Return a new TrackedRawDataElement instance."""
        tracked = super().__new__(cls, *args, **kwargs)
        tracked.id_ = id_
        tracked.original = RawDataElement(*args, **kwargs)
        tracked.events = []
        return tracked

    def _replace(self, silent=False, **kwargs) -> "TrackedRawDataElement":
        """Extend namedtuple _replace with change event tracking."""
        # The `silent` arg exists specifically so that our fixer format did not need to
        # change even though pydicom now splits up fixers into VR and value fixers.
        # To maintain both the current fixer logic and event logging, we need a
        # "silent" change in between fixer sets.
        # Potential future improvement: change the event logging to better mesh with
        # updated pydicom behavior, so that there's no need to have a "silent" arg.
        if not silent:
            for key, val in kwargs.items():
                old = getattr(self, key)
                event = ReplaceEvent(field=key, old=old, new=val)
                self.events.append(event)
        raw = super()._replace(**kwargs)  # calls new
        # NOTE updating the extra namedtuple attrs
        raw.original = self.original
        raw.events = self.events
        raw.id_ = self.id_
        return raw

    def export(self) -> dict:
        """Return the original dataelem, the events and the final version as a dict."""
        return {
            "original": self.original,
            "events": self.events,
            "final": self,
        }


def filter_none_vr_replacement(event: ReplaceEvent) -> bool:
    """Return True except for VR=None replacement events."""
    return not (event.field == "VR" and event.old is None)


class ReadContext:
    """Tracker for RawDataElement change events within a dataset."""

    def __init__(self):
        """Initializes the tracker instance."""
        self.dataelem_dict: t.Dict[int, TrackedRawDataElement] = {}
        self.modified_attrs = Dataset()
        self.nonconforming_elems = Sequence()
        self.oas_idx: t.Optional[int] = None
        self.encoding: t.Optional[t.Union[str, t.List[str]]] = None

    @classmethod
    def from_callback_kwargs(cls) -> "ReadContext":
        """Return read context from the current callback kwargs."""
        return hooks.raw_element_kwargs.get(READER) or cls()

    @property
    def data_elements(self) -> t.List[TrackedRawDataElement]:
        """Expose data_elements as a list for backwards compat."""
        return list(self.dataelem_dict.values())

    def track(
        self, raw: RawDataElement
    ) -> t.Union[RawDataElement, TrackedRawDataElement]:
        """Return a TrackedRawDataElement from a RawDataElement.

        NOTE: We need to use hash, and not ID to store the unique id.  hash
        looks at the values of the object, whereas id looks at the location in
        memory.  id is guarenteed to be unique while objects overlap in
        lifetime, but due to this implementation, RawDataElements won't be
        overlapping in life time, and due to RawDataElement being a namedtuple
        with a very definite size, they are often stored at the same location in
        memory.  So you can end up with id returning the same value for two
        different RawDataElements.

        Args:
            raw (RawDataElement): Input data element

        Returns:
            t.Union[RawDataElement, TrackedRawDataElement]: Output, tracked or not
                based on configuration
        """
        # Store a unique id for each Tracked element, and use it to update the
        # _data_element_dict on Tracker
        # This needs to be `hash`, not `id`, see note above
        dict_key = hash(raw)
        # Can't actually think of a use case here.  We'd have to be calling
        # `track` on the same RawDataElement again, which would have already
        # been decoded.
        if dict_key in self.dataelem_dict:
            return self.dataelem_dict[dict_key]  # pragma: no cover
        tracked_elem = TrackedRawDataElement(*raw, id_=dict_key)
        self.dataelem_dict[dict_key] = tracked_elem
        return tracked_elem

    def update(self, tr_raw: TrackedRawDataElement) -> None:
        """Update a TrackedRawDataElement."""
        self.dataelem_dict[tr_raw.id_] = tr_raw

    def trim(self, event_filter: t.Optional[t.Callable] = None) -> None:
        """Filter tracked events and remove data elements without any changes."""
        if not event_filter:
            event_filter = filter_none_vr_replacement
        for key in list(self.dataelem_dict):
            de = self.dataelem_dict[key]
            de.events = [evt for evt in de.events if event_filter(evt)]
            if not de.events:
                self.dataelem_dict.pop(key)

    def __enter__(self):
        """Enter context.

        Save original pydicom data element callback kwargs, add self to the
        kwargs so data element fixers can access.
        """
        callback_kwargs = hooks.raw_element_kwargs
        self.orig_read_ctx = callback_kwargs.get(READER)
        callback_kwargs[READER] = self
        return self

    def __exit__(self, *args, **kwargs):
        """Exit context.

        Restore original callback kwargs.
        """
        callback_kwargs = hooks.raw_element_kwargs
        callback_kwargs[READER] = self.orig_read_ctx

    def add_nonconforming_elem(
        self,
        tag: BaseTag,
        val: bytes,
        idx: int = 0,
    ):
        """Add an element to the NonConformingElementSequence.

        If an original element was non conforming, add it here.

        Args:
            nonconform (Sequence): NonConformingModifiedAttributesSequence
                ref: PS3.3, C.12.1.1.9.2
            modified (Sequence): ModifiedAttributesSequence
            tag (BaseTag): Tag of nonconforming element
            val (bytes): Value of nonconforming element
            idx (int, optional): If the elements VM !==1, this refers to the index
                (1-indexed, since 0 refers to the whole value). Defaults to 0.
        """
        # NOTE: More to add here if we want, also supports private
        # tags with a specific creator, etc.
        elem = Dataset()
        # ref: PS3.3, 10.17
        elem.SelectorAttribute = tag
        # TODO: If element is in a sequence, list of pointers to sequence item
        # el.SelectorSequencePointer = None
        # Not reporting multiple non-conforming elements in a vm > 1 el.
        # Simply report a problem with the whole element at idx 1
        elem.SelectorValueNumber = idx
        elem.NonconformingDataElementValue = val
        self.nonconforming_elems.append(elem)
        try:
            # Set validation_mode to 0 to allow pydicom to cast empty string to
            # the correct VR
            elem = DataElement(tag, dictionary_VR(tag), "", validation_mode=0)
            self.modified_attrs[tag] = elem
        except KeyError:
            # Private tag, skip updating ModifiedAttributesSequence
            pass

    def add_modified_elem(
        self, elem: t.Union[t.Tuple[BaseTag, str, bool], RawDataElement]
    ):
        """Add a modified data element.

        Args:
            elem ((Tracked)RawDataElement): Tracked or Raw data element.
        """
        # NOTE: This still isn't fully compliant: "f an Attribute within a Sequence
        # was replaced, added or removed, the entire prior value of the Sequence
        # shall be placed in the Modified Attributes Sequence (0400,0550); this
        # applies recursively up to the enclosing Sequence Attribute in the top
        # level Data Set."

        # TODO: Need to not add modified elemetns for data elements that are already in the modifuied elements sequence.  Need dataset context
        buffer = DicomBytesIO()
        buffer.is_little_endian = True
        buffer.is_implicit_VR = False
        tag: BaseTag = Tag(0)
        VR: t.Optional[str] = None
        val: t.Any = None
        raw_val: bytes = b""
        try:
            if len(elem) == 3:
                # Tuple form
                tag, VR, val = elem  # type: ignore
                raw_val = t.cast(bytes, val)
            else:
                orig: RawDataElement = getattr(elem, "original", elem)  # type: ignore
                tag = orig.tag
                VR = t.cast(str, elem.VR)  # type: ignore
                raw_val = orig.value or b""
                val = convert_value(VR, orig, self.encoding)
            VR = t.cast(str, VR)
            validate_value(VR, val, 2)
            de = DataElement(tag, VR, val)
            # Important that we remove all "fixers" here so that we test if the
            # DataElement can be written _as-is_
            with no_fixes():
                write_data_element(buffer, de)
            self.modified_attrs[tag] = DataElement(tag, VR, val)
        except (ValueError, KeyError, OverflowError):
            log.debug(f"value {raw_val!r} for tag {tag:>08x} invalid, writing to {NAS}")
            # If either tag doesn't have VR or if the value is invalid,
            # write to nonconforming sequence
            # During non-strict validation, raw_val may have been changed
            # from bytes to str, and upstream of .add_nonconforming_elem requires
            # bytes, not str
            if not isinstance(raw_val, bytes):
                raw_val = bytes(str(raw_val), "utf-8")  # type: ignore
            self.add_nonconforming_elem(tag, raw_val, 0)

    def process_tracker(self, required_tags: t.Set[int], dataset: Dataset):
        """Handle tracker events and populate modified attributes as necessary."""
        # First look at tracked elements that have been changed, filter them,
        #   and add them to the modified attribute sequences as necessary.
        self.trim()
        have_req_tags = len(required_tags) > 0
        buffer = DicomBytesIO()
        buffer.is_little_endian = True
        buffer.is_implicit_VR = False

        for elem in self.data_elements:
            # NOTE: Distinguish between elements which have been modified and
            # removed, removed being of length 0:
            #
            # As of now, TrackedRawDataElements are only modified by us in
            # the functions the fixer.py module.  These functions _only_ remove
            # the value when it is not parsable, and needs to be added to the
            # NonConforming elements seq
            if elem.length != 0:
                # Value was changed somehow else, but not removed -> go to modified
                if elem.original.value == elem.value and elem.original.VR != elem.VR:
                    continue
                self.add_modified_elem(elem)
                continue

            # NOTE: Should be false if we couldn't get required tags.
            if elem.tag.group == 0x0002 or not have_req_tags:
                safe_to_remove = False
            else:
                safe_to_remove = elem.tag not in required_tags  # type: ignore
            if safe_to_remove:
                self.add_nonconforming_elem(elem.tag, elem.original.value or b"", 0)
                continue
            # Restore original value. If we cannot restore original
            # value, raise.
            log.warning("Would have removed but required so not removing.")
            # Do as little validation as possible, simply try to
            # write and if it fails, raise
            try:
                # NOTE: Any intermediate fixing that happened here
                # before we bailed out (removed the value) will be lost,
                # only the original Value from the dicom will be written
                # back if it can be
                VR = t.cast(str, elem.VR)
                # So that validation_mode is set to do as little validation as possible,
                # it's set to 0 ("IGNORE") here, so that it won't raise if the value
                # doesn't fit DICOM standards, only if it's unable to be parsed at all.
                # If a group 2 element gets in the main dataset, the DICOM can't save...
                if elem.tag.group == 2 and hasattr(dataset, "file_meta"):
                    continue  # pragma: no cover
                out = DataElement(elem.tag, VR, elem.original.value, validation_mode=0)
                write_data_element(buffer, out)
                dataset[out.tag] = out
            except Exception as exc:
                # Writing will fail but we want to warn the user on all DEs that
                # fall into this category
                warnings.warn(
                    (
                        "Could not write original element. Original element "
                        "is required but invalid and cannot be written.\n\n"
                        f"VR: {elem.original.VR}\t value: {elem.original.value!r}\n\n"
                        f"Exception: {exc}"
                    ),
                )

    def update_orig_attrs(self, dataset: Dataset):
        """Update the OriginalAttributesSequence.

        Populate the OriginalAttributesSequence with an entry containing
        the ModifiedAttributesSequence and/or the
        NonconformingModifiedAttributesSequence

        Args:
            dataset (Dataset): Input dataset to add entry, i.e. the
                original DICOM dataset.
        """
        standard = get_standard()
        required_tags = get_required_tags(standard, dataset)
        self.process_tracker(required_tags, dataset)

        # Return early if nothing needs to be done
        if not (len(self.nonconforming_elems) or len(self.modified_attrs)):
            return

        # Get the possibly existing OriginalAttributesSequence in the dataset,
        #   or create.
        oas: Sequence = dataset.setdefault(OAS, Sequence()).value
        # If this is the first time this method has been called during this
        # reading session, we want to create a new entry and update the pointer
        # to the entry we're working with this reading session
        if self.oas_idx is None:
            oas.append(Dataset())
            self.oas_idx = len(oas) - 1
            orig_dat = oas[self.oas_idx]
        # Otherwise, we can just get the entry corresponding to this reading
        # session.
        else:
            orig_dat = oas[self.oas_idx]

        # Once we have the original atrributes sequence entry for this reading
        # session, we can continue with setting the updated metadata and
        # modified attributes.
        setattr(orig_dat, MAS, Sequence([self.modified_attrs]))
        setattr(orig_dat, NAS, self.nonconforming_elems)
        orig_dat.ModifyingSystem = NAME
        orig_dat.ReasonForTheAttributeModification = "CORRECT"

        now = get_datetime().strftime("%Y%m%d%H%M%S.%f%z")
        orig_dat.AttributeModificationDateTime = now
        orig_dat.SourceOfPreviousValues = ""
