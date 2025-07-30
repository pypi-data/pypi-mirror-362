"""PNG file format."""

import re
import struct
import typing as t
import zlib
from collections import Counter
from datetime import datetime

import png
from fw_meta import MetaData
from fw_utils import AnyFile, BinFile
from PIL import Image, PngImagePlugin

from .base import FieldsMixin, File
from .exif import EXIF


class PNG(FieldsMixin, File):
    """PNG file class."""

    def __init__(self, file: AnyFile) -> None:
        """Load and parse PNG files."""
        super().__init__(file)
        with self.file as rfile:
            fields = load_png(rfile)
        img = Image.open(self.file)
        object.__setattr__(self, "fields", fields)
        object.__setattr__(self, "img", img)

    def get_meta(self) -> MetaData:
        """Return the default Flywheel metadata of the PNG."""
        return MetaData({"file.type": "image", "file.name": self.filename})

    @staticmethod
    def canonize_key(key):
        """Return canonized string form for a given field name."""
        return canonize_key(key)

    def save(self, file: t.Optional[AnyFile] = None) -> None:
        """Save (potentially modified) data file."""
        with self.open_dst(file) as wfile:
            pnginfo = PngImagePlugin.PngInfo()
            kwargs = {"pnginfo": pnginfo, "format": "PNG"}
            for chunk in self.fields.values():
                if isinstance(chunk, EXIF):
                    kwargs["exif"] = t.cast(EXIF, self.fields["exif"]).to_bytes()
                else:
                    c_type = chunk.type.encode("ascii")
                    value = chunk.to_bytes()
                    pnginfo.add(c_type, value, after_idat=chunk.after_idat)
            self.img.save(wfile, **kwargs)

    def __setitem__(
        self, key: str, value: t.Union[str, bytes, "BaseChunk", EXIF]
    ) -> None:
        """Set field value by name."""
        key = self.canonize_key(key)
        if ALIASES.get(key, key) in PILLOW_CHUNKS:
            raise KeyError(f"{key} cannot be modified directly, instead use img attr")
        if isinstance(value, (BaseChunk, EXIF)):
            self.fields[key] = value
        elif isinstance(value, str):
            self.fields[key] = iTXt(key, value)
        elif isinstance(value, bytes):
            assert len(key) == 4, "expected 4 bytes length key for byte values"
            if key in DECODERS:
                value = DECODERS[key](value)
            else:
                value = Chunk(ALIASES.get(key, key), value)
            self.fields[key] = value
        else:
            raise ValueError("Unexpected value type")


def load_png(file: BinFile) -> t.Dict[t.Union[int, str], t.Any]:
    """Parse PNG file."""
    file.seek(0)
    reader = png.Reader(file=file)
    fields: t.Dict[t.Union[int, str], t.Any] = {}
    counter: t.Counter[str] = Counter()
    after_idat = False
    for c_type, value in reader.chunks():
        c_type = c_type.decode("ascii")
        if c_type == "IDAT":
            after_idat = True
        if c_type in PILLOW_CHUNKS:
            continue
        key = canonize_key(c_type)
        if key in DECODERS:
            chunk = DECODERS[key](value)
        else:
            chunk = Chunk(c_type, value)
        if isinstance(chunk, BaseChunk):
            chunk.after_idat = after_idat
        key = getattr(chunk, "key", key)
        key = canonize_key(key)
        if counter[key]:
            key = f"{key}_{counter[key]}"
        counter[key] += 1
        fields[key] = chunk
    return fields


class BaseChunk:
    """Base chunk class."""

    type: str
    after_idat: bool = False


class Chunk(BaseChunk, bytes):
    """General PNG chunk as bytes."""

    @staticmethod
    def __new__(cls, c_type, text):
        """Create tEXt chunk object."""
        self = bytes.__new__(cls, text)
        self.type = c_type
        return self

    def to_bytes(self) -> bytes:
        """Return chunk as bytes."""
        return self


class tEXt(BaseChunk, str):
    """tEXt chunk."""

    type = "tEXt"
    key: str

    @staticmethod
    def __new__(cls, key, text):
        """Create tEXt chunk object."""
        self = str.__new__(cls, text)
        self.key = key
        return self

    @classmethod
    def from_bytes(cls, value: bytes) -> "tEXt":
        """Parse and return chunk from bytes."""
        key_b, _, text_b = value.partition(b"\0")
        key = key_b.decode("latin-1")
        text = text_b.decode("latin-1", "replace")
        return cls(key, text)

    def to_bytes(self) -> bytes:
        """Return chunk as bytes."""
        return self.key.encode("latin-1") + b"\0" + self.encode("latin-1")


class zTXt(BaseChunk, str):
    """zTXt chunk."""

    type = "zTXt"
    key: str

    @staticmethod
    def __new__(cls, key: str, text: str):
        """Create zTXt chunk object."""
        self = str.__new__(cls, text)
        self.key = key
        return self

    @classmethod
    def from_bytes(cls, value: bytes) -> "zTXt":
        """Parse and return chunk from bytes."""
        key_b, _, rest = value.partition(b"\x00")
        key = key_b.decode("latin-1")
        text = zlib.decompress(rest[1:]).decode("latin-1", "replace")
        return cls(key, text)

    def to_bytes(self) -> bytes:
        """Return chunk as bytes."""
        val = self.encode("latin-1")
        return self.key.encode("latin-1") + b"\0\0" + zlib.compress(val)


class iTXt(BaseChunk, str):
    """iTXt chunk."""

    type = "iTXt"
    key: str
    t_key: str
    lang: str
    zip: bool

    @staticmethod
    def __new__(  # noqa PLR0913
        cls, key, text, t_key: str = "", lang: str = "", zip_: bool = False
    ) -> "iTXt":
        """Create iTXt chunk object."""
        self = str.__new__(cls, text)
        self.key = key
        self.t_key = t_key
        self.lang = lang
        self.zip = zip_
        return self

    @classmethod
    def from_bytes(cls, value: bytes) -> "iTXt":
        """Parse and return chunk from bytes."""
        key_b, rest = value.split(b"\0", 1)
        cf, cm, rest = rest[0], rest[1], rest[2:]
        lang_b, t_key_b, text_b = rest.split(b"\0", 2)
        zip_ = cf != 0 and cm == 0
        if zip_:
            text_b = zlib.decompress(text_b)
        key = key_b.decode("latin-1")
        lang = lang_b.decode("utf-8")
        t_key = t_key_b.decode("utf-8")
        text = text_b.decode("utf-8")
        return cls(key, text, t_key, lang, zip_)

    def to_bytes(self) -> bytes:
        """Return chunk as bytes."""
        key = self.key.encode("latin-1", "strict")
        compression = b"\0\0\0"
        lang = self.lang.encode("utf-8", "strict")
        t_key = self.t_key.encode("utf-8", "strict")
        value = self.encode("utf-8", "strict")
        if self.zip:
            value = zlib.compress(value)
            compression = b"\0\x01\0"
        return key + compression + lang + b"\0" + t_key + b"\0" + value


class tIME(BaseChunk, datetime):
    """tIME chunk."""

    type: str = "tIME"
    key: str = "time"

    @classmethod
    def from_bytes(cls, value: bytes) -> "tIME":
        """Parse and return chunk from bytes."""
        return cls(*struct.unpack(">HBBBBB", value))

    def to_bytes(self) -> bytes:
        """Return chunk as bytes."""
        return struct.pack(
            ">HBBBBB",
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
        )


def canonize_key(key):
    """Return canonized string form for a given field name."""
    return re.sub(r"[^a-zA-Z0-9]", "_", key.strip().lower())


DECODERS: t.Dict[str, t.Callable] = {
    "itxt": iTXt.from_bytes,
    "text": tEXt.from_bytes,
    "ztxt": zTXt.from_bytes,
    "time": tIME.from_bytes,
    "exif": EXIF.from_bytes,
}

# sources:
# http://ftp-osl.osuosl.org/pub/libpng/documents/png-1.2-pdg.html#C.Summary-of-standard-chunks
# http://ftp-osl.osuosl.org/pub/libpng/documents/pngext-1.5.0.html#Summary
# NOTE the following extension chunk types not supported by pillow and will be lost when
# saving the file: oFFs, pCAL, sCAL, gIFg, gIFt, gIFx, sTER, dSIG, fRAc
CHUNK_TYPES = [
    # critical chunks
    "IHDR",
    "PLTE",
    "IDAT",
    "IEND",
    # ancillary chunks
    "cHRM",
    "gAMA",
    "iCCP",
    "sBIT",
    "sRGB",
    "bKGD",
    "hIST",
    "tRNS",
    "pHYs",
    "sPLT",
    "tIME",
    "iTXt",
    "tEXt",
    "zTXt",
    # extensions
    "eXIf",
]


ALIASES = {canonize_key(t): t for t in CHUNK_TYPES}


# chunks that controlled and written by Pillow
PILLOW_CHUNKS = [
    "IHDR",
    "PLTE",
    "IDAT",
    "IEND",
    "iCCP",
    "tRNS",
    "pHYs",
]
