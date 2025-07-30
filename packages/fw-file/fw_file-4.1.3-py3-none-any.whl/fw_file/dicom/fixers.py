"""DataElement Fixers."""

import logging
import re
import typing as t

import pydicom.config as pydicom_config
import pydicom.dataelem as pydicom_dataelem
import pydicom.hooks as pydicom_hooks
from dateutil.parser import ParserError, parse
from pydicom.charset import decode_bytes, default_encoding, encode_string
from pydicom.datadict import dictionary_VR, get_entry
from pydicom.dataelem import DataElement, RawDataElement
from pydicom.dataset import Dataset
from pydicom.multival import MultiValue
from pydicom.valuerep import (
    AMBIGUOUS_VR,
    MAX_VALUE_LEN,
    TEXT_VR_DELIMS,
    DSclass,
    format_number_as_ds,
)
from pydicom.values import convert_value, validate_value

from .config import get_config
from .utils import generate_uid

log = logging.getLogger(__name__)


private_vr_for_tag = pydicom_hooks._private_vr_for_tag
LUT_DESCRIPTOR_TAGS = pydicom_dataelem._LUT_DESCRIPTOR_TAGS
VM_RANGE_RE = re.compile(r"^(\w+)-(\w+)$")
# pylint: enable=protected-access


def char_range(a: str, b: str) -> t.List[str]:
    """Create a range of characters using ascii int values."""
    return [chr(v) for v in range(ord(a), ord(b) + 1)]


def tag_specific_fixer(
    raw: RawDataElement,
    **_kwargs,
) -> RawDataElement:
    """Fixes for known specific tags.

    NOTE: By definition, VR changes do not go in the OriginalAttributesSequence,
    ref: PS3.3, C.12.1.1.9
    """
    # make sure that SpecificCharacterSet has correct VR
    # ref: PS3.6, chapter 6
    if raw.tag == 0x00080005 and raw.VR != "CS":
        raw = raw._replace(VR="CS")
    return raw


def apply_dictionary_VR(
    raw: RawDataElement, dataset: t.Optional[Dataset] = None, **_kwargs
) -> RawDataElement:
    """Replace VR with VR found in the public or private dictionaries.

    By definition, VR changes do not go in the OriginalAttributesSequence,
    ref: PS3.3, C.12.1.1.9

    NOTE: Output of this function is guaranteed to have a known VR since it
    either comes from dictionary_VR, private_vr_for_tag, is set to "UL"/"UN"
    """
    VR = raw.VR
    # After this, VR is guaranteed to be string, not None
    if not VR:
        VR = "UN"
    try:
        VR = dictionary_VR(raw.tag)
    except KeyError:
        # Only set private tag VR if it is known in the private tag dictionary,
        # AND if the found VR is _unknown_. Later in convert_exception_fixer, we
        # will override the found VR with the dictionary VR but only if there is
        # a converter exception trying to read the value given the VR in the
        # dicom.
        if raw.tag.is_private:
            # VRs for private tags see PS3.5, 6.2.2
            new_VR = private_vr_for_tag(dataset, raw.tag)
            # Python 3.11 changed enums returning the enum type instead of string value
            new_VR = getattr(new_VR, "value", new_VR)
            # private_vr_for_tag returns UN if nothing found.
            # only update VR if something is found
            if new_VR != "UN" and VR == "UN":
                VR = new_VR
        # group length tag implied in versions < 3.0
        elif raw.tag.element == 0:
            VR = "UL"
        else:
            VR = "UN"
    if VR != raw.VR:
        # Pydicom stores Item/SequenceDelimitationItem VRs as 'NONE'. They don't
        # technically have a VR but in order to avoid issues in
        # converter_exception_fixer, set it to OB (other bytes)
        if VR == "NONE":
            VR = "OB"
        if VR in AMBIGUOUS_VR:
            candidates = VR.split(" or ")
            if raw.VR in candidates:
                return raw
            # Otherwise, leave it ambiguous, it will be rectified by calling
            # pydicom.filewriter.correct_ambiguous_vr_element on save
        raw = raw._replace(VR=VR)
    return raw


# TBD wouldn't an allow-list be simpler/shorter?
# http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
backslash_compatible_VRs = (
    "AT,DS,FD,FL,IS,LT,OB,OB/OW,OB or OW,OF,OW,OW/OB,OW or OB,SL,SQ,SS,ST,UL,UN,US,UT"
).split(",")


def replace_backslash_in_VM1_str(
    raw: RawDataElement,
    **_kwargs,
) -> RawDataElement:
    r"""Replace invalid \ characters with _ in string VR values of VM=1."""
    try:
        VR, VM, *_ = get_entry(raw.tag)
    except KeyError:
        return raw
    if VM == "1" and VR == raw.VR and VR not in backslash_compatible_VRs:
        value = raw.value
        if value and b"\\" in value:
            to_add = value.replace(b"\\", b"_")
            # NOTE: Don't need to update length because subbing 1-char for 1-char
            #   length stays the same
            raw = raw._replace(value=to_add)
    return raw


def crop_text_VR(
    raw: RawDataElement,
    **kwargs,
) -> RawDataElement:
    """Crop text VRs which are too long."""
    value = kwargs.get("value", raw.value)
    if raw.VR in MAX_VALUE_LEN and value:
        VR = t.cast(str, raw.VR)
        max_len = MAX_VALUE_LEN[VR]
        if len(value) > max_len:
            # NOTE: this is not valid according to dicom standard
            # Instead of cropping, we should just remove this value
            # and add to Nonconforming modified attributes sseuqnece
            cropped = value[:max_len]
            raw = raw._replace(value=cropped, length=len(cropped))
            return raw
    return raw


def convert_exception_fixer(
    raw: RawDataElement,
    encoding: t.Optional[t.Union[str, t.List[str]]] = None,
    dataset: t.Optional[Dataset] = None,
    **_kwargs,
) -> RawDataElement:
    """FW File convert_value handler.

    Will perform the following:
      - try loading elements with user-specified fallback VRs on failure
      - when all else fails, use VR=OB to just load the value as bytes
    """

    def empty():
        """Remove value and add to NonconformingAttributesSequence."""
        nonlocal raw
        raw = raw._replace(value="", length=0)
        return convert_exception_fixer(raw, encoding, dataset)

    VR = t.cast(str, raw.VR)
    value = None
    try:
        # Need to call both convert_value and DataElement Constructor here
        # because _some_ VRs have their `validate`
        # method called in `convert_value` and _some_ only have it called in
        # their `DataElement` constructor.
        #
        # For example, for the DA VR, convert_value returns a
        # pydicom.values.MultiString, which doesn't validate the actual format
        # of the value, only whether the value can be loaded into a
        # MultiString.
        #
        # Then the DataElement constructor actually constructs the VR class
        # which sees if the value can be loaded into a datetime
        #
        # References:
        #
        # DA converter called in convert_value:
        # https://github.com/pydicom/pydicom/blob/v2.2.2/pydicom/values.py#L170
        #
        # DA VR class instantiated:
        # https://github.com/pydicom/pydicom/blob/v2.2.2/pydicom/dataelem.py#L543

        value = convert_value(VR, raw, encoding)
        DataElement(
            raw.tag,
            VR,
            value,
            validation_mode=pydicom_config.settings.reading_validation_mode,
        )
    except (ValueError, OverflowError, TypeError, NotImplementedError):
        # Only attempt to apply dictionary VR for a private tag if initial value
        # conversion didn't work. Private tag dictionary VRs don't seem to
        # always be accurate, and in fact there is nothing stopping
        # manufacturers from changing their internal "VR" for this field. So we
        # should only rely on the dictionary as a last resort to give us a hint
        # what the field should be if we can't decode it at first
        if raw.tag.is_private:
            # VRs for private tags see PS3.5, 6.2.2
            new_VR = private_vr_for_tag(dataset, raw.tag)
            # Python 3.11 changed enums returning the enum type instead of string value
            new_VR = getattr(new_VR, "value", new_VR)
            # private_vr_for_tag returns UN if nothing found.
            # only update VR if something is found
            if new_VR not in {"UN", VR}:
                # If we found a new VR, try converting again
                VR = new_VR
                raw = raw._replace(VR=new_VR)
                return convert_exception_fixer(raw, encoding, dataset)

        # If we get a value error, it could be caused by either validate_value
        # or convert_value. Regardless, something is wrong with the value, so we
        # attempt to fix it.
        fixed_val = fix_invalid_VR_value(VR, raw, encoding=encoding, dataset=dataset)
        try:
            # Avoid calling TrackedRawDataElement._replace here since we
            # don't want this value change tracked
            fixed_raw_elem = RawDataElement._replace(raw, value=fixed_val)
            value = convert_value(VR, fixed_raw_elem, encoding)
            DataElement(
                raw.tag,
                VR,
                fixed_val,
                validation_mode=pydicom_config.settings.reading_validation_mode,
            )
            # Replace value if fixed.
            if fixed_val != raw.value:
                # NOTE: Can't think of a case where this wouldn't be true.
                if len(fixed_val or b"") != len(raw.value or b""):
                    raw = raw._replace(length=len(fixed_val or b""))
                raw = raw._replace(value=fixed_val)
        except ValueError:
            if get_config().read_only:
                # In read-only mode, invalid values are saved with VR=OB
                # as a last resort instead of removing the value.
                raw = raw._replace(VR="OB")
            else:
                # In normal RW mode,
                # If we still get an error after using fixed value, bail.
                return empty()
        return convert_exception_fixer(raw, encoding, dataset)
    except Exception:
        log.exception("Unhandled exception.", exc_info=True)
        # Any other unforeseen exception in conversion
        return empty()
    return raw


def fix_uids(
    raw: RawDataElement, encoding: t.List[str], **_kwargs
) -> t.Optional[bytes]:
    """Attempt to fix an invalid UID.

    * Determine if UID "looks" valid
    * If so, use this value as only entropy source to generate new UID
    (deterministic)
    * Otherwise, generate a new UID
    """
    VALID_THRESHOLD = 0.8
    FIX_TAGS = (
        (0x0002, 0x0003),  # MediaStorageSOPInstanceUID
        (0x0020, 0x000E),  # SeriesInstanceUID
        (0x0020, 0x000D),  # StudyInstanceUID
        (0x0020, 0x0052),  # FrameOfReferenceUID
        (0x0008, 0x0018),  # SOPInstanceUID
        (0x0008, 0x1155),  # ReferencedSOPInstanceUID
    )

    if raw.tag not in FIX_TAGS:
        return raw.value

    val = raw.value.strip(b"\x00").decode()  # type: ignore
    tmp = []
    for part in val.split("."):
        tmp.append(part.lstrip("0") if part != "0" else part)
    new = ".".join(tmp)
    # Try to validate value stripped of 0's
    try:
        validate_value("UI", new, validation_mode=2)
        return encode_string(new, encodings=encoding)
    except ValueError:
        pass
    # Assume not valid if length is less than 5
    if len(new) > 5:
        # If all characters are numbers or periods, it "looks" valid
        allowed_chars = [*char_range("0", "9"), "."]
        valid = 0
        for c in new:
            if c in allowed_chars:
                valid += 1
        # If more than xx% of characters are valid, assume it "looks" like a UID
        if float(valid) / float(len(new)) > VALID_THRESHOLD:
            return encode_string(generate_uid(entropy_srcs=[new]), encodings=encoding)
    return encode_string(generate_uid(), encodings=encoding)


def fix_datetimes(
    raw: RawDataElement, encoding: t.List[str], **_kwargs
) -> t.Optional[bytes]:
    """Attempt to parse an invalid date and format correctly."""
    # TZ handling could be added by splitting on "-" or "+" if needed
    try:
        date = parse(raw.value.decode())  # type: ignore
        if raw.VR == "DA":
            fmt_dt = date.strftime("%Y%m%d")
        elif raw.VR == "DT":
            fmt_dt = date.strftime("%Y%m%d%H%M%S.%f%z")
            fmt_dt = fmt_dt.rstrip("0")
        else:
            fmt_dt = date.strftime("%H%M%S.%f%z")
            fmt_dt = fmt_dt.rstrip("0")
        if fmt_dt[-1] == ".":
            fmt_dt += "0"
        return encode_string(fmt_dt, encodings=encoding)
    except (ParserError, OverflowError):
        return raw.value


def fix_age_string(
    raw: RawDataElement, encoding: t.List[str], **_kwargs
) -> t.Optional[bytes]:
    """Fixer for Age Strings (AS).

    Ensure one of D,W,M,Y is at end of the string, and pad to 4 characters.

    If no time quantifier is present, assume Years, this is in line with
    fw_file.dicom.utils.get_session_age.
    """
    age_str = raw.value.decode().upper()  # type: ignore
    match = re.match(r"(?P<value>[0-9]+)(?P<scale>[dwmyDWMY]*)", age_str)
    if match:
        # Pad value to 3 chars with preceding 0s
        new_val = match.group("value").lstrip("0")
        if len(new_val) > 3 or (match.group("scale") and len(match.group("scale")) > 1):
            # Don't want to lose information, but not valid, just return and let VR
            # be set to OB
            return raw.value
        pad = 3 - len(new_val)
        if pad:
            new_val = "0" * pad + new_val
        new_val += match.group("scale") if match.group("scale") else "Y"
        return encode_string(new_val, encodings=encoding)
    return raw.value


def fix_number_strings(
    raw: RawDataElement,
    encoding: t.List[str],
    **_kwargs,
) -> t.Optional[bytes]:
    """Fix DS (Decimal String).

    * Remove invalid characters
    * Auto-format overflowed DS
    """
    # DS allowed characters
    allowed = [*char_range("0", "9"), "E", "e", ".", "+", "-", " "]
    # Decode string and strip null-bytes from the end
    # NOTE: Assertion that raw.value is not None in fix_invalid_VR_value
    num_string = raw.value.decode(default_encoding)  # type: ignore
    num_string.rstrip(" \x00")
    # Rebuild string by removing invalid characters and formatting individual components.
    new_parts = []
    for part in num_string.split("\\"):
        component = "".join(c if c in allowed else "" for c in part)
        try:
            new_parts.append(format_number_as_ds(float(component)))
        except ValueError:
            return raw.value

    # Re-encode bytes for passing into DataElement
    new_val = encode_string("\\".join(new_parts), encodings=encoding)
    # If still not valid, return original value, will raise in convert_exception_fixer
    try:
        DataElement(raw.tag, "DS", new_val)
    except (ValueError, OverflowError):  # pragma: no cover
        # Can't think of a test case that would trigger this.
        return raw.value
    # Fix decimal value in IS
    if raw.VR == "IS":
        # Try to convert as DS
        tmp = RawDataElement._replace(raw, value=new_val)
        value = convert_value("DS", tmp)
        # TODO consider logging vs warnings, apply as needed
        if isinstance(value, (MultiValue, list, tuple)):
            value = "\\".join((str(int(v)) for v in value))
        else:
            assert isinstance(value, DSclass)
            value = str(int(value))
        return encode_string(value, encodings=encoding)

    return new_val


def fix_invalid_char(
    raw: RawDataElement,
    encoding: t.List[str],
    upper: bool = False,
    **_kwargs,
) -> t.Optional[bytes]:
    """Attempt to remove non-printable characters from byte decoding."""
    orig_validation_mode = pydicom_config.settings.reading_validation_mode
    pydicom_config.settings.reading_validation_mode = 0
    assert isinstance(raw.value, bytes)
    val = decode_bytes(raw.value, encodings=encoding, delimiters=TEXT_VR_DELIMS)
    new_val = ""
    for char in val:
        new_val += char if char.isprintable() else "_"
    if upper:
        new_val = new_val.upper()
    pydicom_config.settings.reading_validation_mode = orig_validation_mode
    return encode_string(new_val, encodings=encoding)


VR_FIXERS = {
    "DA": (fix_datetimes, {}),
    "DT": (fix_datetimes, {}),
    "TM": (fix_datetimes, {}),
    "AS": (fix_age_string, {}),
    "UI": (fix_uids, {}),
    "DS": (fix_number_strings, {}),
    "IS": (fix_number_strings, {}),
    "SH": (fix_invalid_char, {}),
    "LO": (fix_invalid_char, {}),
    "ST": (fix_invalid_char, {}),
    "PN": (fix_invalid_char, {}),
    "LT": (fix_invalid_char, {}),
    "UC": (fix_invalid_char, {}),
    "UT": (fix_invalid_char, {}),
    "CS": (fix_invalid_char, {"upper": True}),
}


def fix_invalid_VR_value(
    VR: str,
    raw: RawDataElement,
    dataset: t.Optional[Dataset] = None,
    encoding: t.Optional[t.Union[str, t.List[str]]] = None,
) -> t.Optional[bytes]:
    """Try to fix an invalid value for the given VR.

    Returns:
        Either a fixed value, or the original
    """
    # DICOM VR reference
    # https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html

    # Date, Datetime, Time
    if not encoding:
        encoding = [default_encoding]  # pragma: no cover
    elif not isinstance(encoding, list):
        encoding = [encoding]  # pragma: no cover
    assert raw.value
    if VR in VR_FIXERS:
        fixer, kwargs = VR_FIXERS[VR]
        return fixer(raw, dataset=dataset, encoding=encoding, **kwargs)  # type: ignore
    return raw.value  # pragma: no cover


def LUT_descriptor_fixer(
    raw: RawDataElement,
    **kwargs,
) -> RawDataElement:
    """Fix LUT Descriptor tags."""
    # Value has already been converted, so value is a native python type,
    # not bytes
    if raw.tag in LUT_DESCRIPTOR_TAGS:
        VR = t.cast(str, raw.VR)
        value = convert_value(VR, raw, kwargs.get("encoding"))
        try:
            if value[0] < 0:
                # NOTE: Pydicom uses 2**16, but that seems wrong to me.  The
                # first element can't be < 0 but other elements can be.  If the
                # first element is 0, we want to make it positive, even when it
                # can be a signed integer.  Adding 2**16 either causes an
                # overflow, or makes it signed negative.  So add 2**15 so it is
                # guaranteed to be a signed positive
                # https://github.com/pydicom/pydicom/blob/v2.3.0/pydicom/dataelem.py#L881
                value[0] += 1 << 15  # type: ignore
                b_args = (2, "little" if raw.is_little_endian else "big")
                b_kwargs = {"signed": True}
                new_val = (
                    (value[0]).to_bytes(*b_args, **b_kwargs)
                    + (value[1]).to_bytes(*b_args, **b_kwargs)
                    + (value[2]).to_bytes(*b_args, **b_kwargs)
                )
                raw = raw._replace(value=new_val)
                if len(new_val) != len(value):
                    raw = raw._replace(length=len(new_val))
        except TypeError:  # pragma: no cover
            pass
    return raw
