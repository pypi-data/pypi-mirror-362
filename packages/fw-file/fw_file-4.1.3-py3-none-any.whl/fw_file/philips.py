"""Philips MR / PARREC header (.par) file format."""

import os
import re
import shutil
import tempfile
import typing as t
import zipfile
from datetime import datetime
from decimal import Decimal, InvalidOperation

import dateutil.parser as dt_parser
from fw_meta import MetaData
from fw_utils import BinFile

from .base import AnyFile, FieldsMixin, File

PAR_FIELD_RE = r"^\.\s+(?P<name>\w[^:]+).*?:\s*(?P<value>.*)$"
PAR_KEY_RE = r"^(?P<key>[-\.\w\s/]+).*$"


class PARFile(FieldsMixin, File):
    """Philips MR / PARREC header (.par) file format."""

    def __init__(self, file: AnyFile) -> None:
        """Read and parse a Philips MR image header / PAR file.

        Args:
            file (str|Path|file): Filepath (str|Path) or open file to read from.
        """
        super().__init__(file)
        with self.file as rfile:
            object.__setattr__(self, "fields", load_par(rfile))

    @classmethod
    def from_zip(cls, archive: AnyFile) -> "PARFile":
        """Return PAR file from a ZIP archive.

        Args:
            archive: ZIP archive path or readable to extract and parse.
        """
        tempdir = tempfile.mkdtemp()
        with zipfile.ZipFile(archive, mode="r") as zfile:  # type: ignore[arg-type]
            zfile.extractall(tempdir)
        extracted_files = os.listdir(tempdir)
        par = None
        for f in extracted_files:
            if f.lower().endswith(".par"):
                par = cls(os.path.join(tempdir, f))
        shutil.rmtree(tempdir)
        if not par:
            raise FileNotFoundError("No PAR file found in zip.")
        return par

    # This does not currently support saving back to a zip archive,
    # but a future thought for a .to_zip() method would be to have
    # the original archive passed in as an arg, extract, update PAR,
    # and then zip it all back up.

    def get_meta(self) -> MetaData:
        """Return the default Flywheel metadata."""
        meta: dict = {
            "subject.label": self.get("patient_name"),
            "session.label": self.get("examination_name"),
            "acquisition.label": get_acquisition_label(self),
            "acquisition.timestamp": get_acquisition_timestamp(self),
            "file.type": "parrec",
            "file.name": self.filename,
        }
        return MetaData(meta)

    @staticmethod
    def canonize_key(key: str) -> str:
        """Return canonized string form for a given field name."""
        return canonize_key(key)

    def save(self, file: AnyFile = None) -> None:
        """Save modified data file."""
        just_len = max(
            len(f["name"]) for f in self.fields.values() if isinstance(f, dict)
        )
        with self.open_dst(file) as wfile:
            for val in self.fields.values():
                if isinstance(val, str):
                    wfile.write(val.encode())
                    continue
                name = val["name"].ljust(just_len)
                val = val["value"]
                if isinstance(val, list):
                    # double space used in most of the example PAR files
                    val = "  ".join([str(v) for v in val])
                if val is None:
                    val = ""
                wfile.write(f".    {name}:   {val}\n".encode())

    def __getitem__(self, key: str):
        """Get field value by tag/keyword."""
        return self.fields[canonize_key(key)]["value"]

    def __setitem__(self, key: str, value) -> None:
        """Set field value by tag/keyword."""
        key = canonize_key(key)
        if key not in self.fields:
            raise KeyError("Invalid key")
        self.fields[key]["value"] = value


def load_par(file: BinFile) -> t.Dict[t.Union[int, str], t.Any]:
    """Parse PAR file.

    Return parsed PAR file as a dictionary. General info fields are parsed
    as name/value and available via a canonized key. For other lines we just store
    the raw line and use the line number as key.
    """
    parsed: t.Dict[t.Union[int, str], t.Any] = {}
    for line_no, line_bytes in enumerate(file):
        line = line_bytes.decode()
        match = re.match(PAR_FIELD_RE, line)
        if match:
            name = match.group("name").strip()
            value = match.group("value").strip()
            value = parse_value(value) if value else None
            key = canonize_key(name)
            parsed[key] = {"name": name, "value": value}
        else:
            parsed[line_no] = line
        line_no += 1
    return parsed


def parse_value(value: str):
    """Return parsed Bruker ParaVision field value.

    Try parse value string as list of integers and decimals,
    fallback to the original str. Return single value if the
    list contains only one item.
    """
    parsed_val: t.Any = None
    parts = value.split()
    # try as integer
    try:
        parsed_val = [int(v) for v in parts]
    except ValueError:
        pass
    # try as decimal
    if not parsed_val:
        try:
            parsed_val = [Decimal(v) for v in parts]
        except InvalidOperation:
            pass
    # fallback to the original value
    if not parsed_val:
        return value
    if isinstance(parsed_val, list) and len(parsed_val) == 1:
        parsed_val = parsed_val[0]
    return parsed_val


def canonize_key(key: str) -> str:
    """Return canonized string form for a given field name."""
    match = re.match(PAR_KEY_RE, key)
    if match:
        return re.sub(r"[^a-zA-Z0-9]", "_", match.group("key").strip().lower())
    raise KeyError("Invalid key")


def get_acquisition_label(par: PARFile) -> t.Optional[str]:
    """Return acquisition label.

    Combination of Protocol name, Acquisition nr and Reconstruction nr.
    """
    fields = ("protocol_name", "acquisition_nr", "reconstruction_nr")
    parts = [str(par[field]) for field in fields if par.get(field)]
    if not parts:
        return None
    return "_".join(parts)


def get_acquisition_timestamp(par: PARFile) -> t.Optional[datetime]:
    """Return acquisition timestamp extracted from Examination date/time field."""
    timestamp = par.get("examination_date_time")
    if not timestamp:
        return None
    try:
        return dt_parser.parse(timestamp)
    except dt_parser.ParserError:  # type: ignore
        return None
