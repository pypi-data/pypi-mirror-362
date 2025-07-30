"""EXIF file format."""

import typing as t

import piexif
from piexif import TAGS

from .base import AttrMixin, FieldsMixin, MutableMapping

# ImageFileDirectory containing the meta information
# https://docs.fileformat.com/image/exif/#image-file-directory
IFDS = ["0th", "Exif", "GPS", "Interop", "1st", "thumbnail"]
IFD_ALIASES = {ifd.lower(): ifd for ifd in IFDS}
# EXIF metadata is stored in ifd/tag format ({"0th": {271: <value>}}),
# where every tag has its keyword name (271 maps to "Make"), so
# KEYWORD_MAP is created to easily navigate and convert between tag and name
KEYWORD_MAP: dict = {}
for ifd_ in IFDS[:-1]:
    for tag_, desc in TAGS[ifd_].items():
        KEYWORD_MAP.setdefault(desc["name"].lower(), {"tag": tag_, "ifds": []})
        KEYWORD_MAP[desc["name"].lower()]["ifds"].append(ifd_)


class EXIF(FieldsMixin, AttrMixin, MutableMapping):
    """Dict like interface for handling EXIF metadata."""

    def __init__(self, **fields):
        """Initialize EXIF instance."""
        object.__setattr__(self, "fields", fields)

    @classmethod
    def from_bytes(cls, value: bytes) -> "EXIF":
        """Parse and return EXIF from bytes."""
        return cls(**piexif.load(value))

    def to_bytes(self) -> bytes:
        """Convert EXIF metadata dict to bytes."""
        return piexif.dump(self.fields)

    def __getitem__(self, key: t.Union[t.Tuple[str, str], str]):
        """Get EXIF value by (ifd, tag)/tag."""
        if key in IFDS or key in IFD_ALIASES:
            key = IFD_ALIASES.get(t.cast(str, key), key)
            return super().__getitem__(t.cast(str, key))
        ifds, tag = get_exif_tag(key)
        # If IFD not provided in key return the first find
        for ifd in ifds:
            value = super().__getitem__(ifd)[tag]
            if value:
                return value
        raise KeyError(f"{key}")  # pragma: no cover

    def __setitem__(self, key: t.Union[t.Tuple[str, str], str], value) -> None:
        """Set EXIF tag's value."""
        if key in IFDS or key in IFD_ALIASES:
            key = IFD_ALIASES.get(t.cast(str, key), key)
            self.fields[key] = value
            return
        ifds, tag = get_exif_tag(key)
        if len(ifds) > 1:
            raise KeyError(f"Ambiguous key, multiple IFDs found: {ifds!r}")
        self.fields.setdefault(ifds[0], {})[tag] = value

    def __delitem__(self, key: t.Union[t.Tuple[str, str], str]) -> None:
        """Delete EXIF tag."""
        if key in IFDS or key in IFD_ALIASES:
            key = IFD_ALIASES.get(t.cast(str, key), key)
            del self.fields[key]
            return
        ifds, tag = get_exif_tag(key)
        for ifd in ifds:
            del self.fields.get(ifd, {})[tag]


def get_exif_tag(key: t.Union[t.Tuple[str, str], str]) -> t.Tuple[t.List[str], int]:
    """Get EXIF tag and IFDs from keyword."""
    ifd = None
    if isinstance(key, tuple):
        assert len(key) == 2, "expected (IFD, TAG) tuple"
        ifd, key = key
    result = KEYWORD_MAP[key.lower()]
    return result["ifds"] if not ifd else [IFD_ALIASES[ifd.lower()]], result["tag"]
