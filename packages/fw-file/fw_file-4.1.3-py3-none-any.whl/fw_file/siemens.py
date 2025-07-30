"""Siemens file formats.

- .dat - MR RAW (read only)
- .ptd - PET RAW
- .rda - MR Spectroscopy
"""

import io
import re
import struct
import typing as t

from fw_meta import MetaData
from fw_utils import BinFile

from .base import AnyFile, FieldsMixin, File, ReadOnly, parse_yaml_value
from .dicom import DICOM, TagType, utils

#######
# DAT #
#######

DAT_HEADER = b"<XProtocol>"
DAT_KEY_RE = r'\."[a-z]*(?P<key>[A-Z][A-Za-z0-9]+)"'
DAT_MOD_RE = r"(<(Precision|MinSize|MaxSize)> \d+|<Limit>\s+\{[^}]+\})?\s*"
DAT_VAL_RE = rf"\s*{{\s*{DAT_MOD_RE}(?P<value>.*?)\s*}}"
DAT_FIELD_RE = rf'\s*<Param[^"]+{DAT_KEY_RE}>{DAT_VAL_RE}'
DAT_ARRAY_RE = rf"\s*<ParamArray{DAT_KEY_RE}>"
DAT_SEX_MAP = {1: "M", 2: "F", 3: "O"}  # TODO verify mapping assumption
DAT_KEY_MAP = {
    "UsedPatientWeight": "PatientWeight",
    "PerfPhysiciansName": "PerformingPhysiciansName",
    "SeriesLOID": "SeriesInstanceUID",
    "StudyComment": "StudyComments",
    "StudyLOID": "StudyInstanceUID",
}


class DATFile(ReadOnly, FieldsMixin, File):
    """Siemens MR RAW (.dat) file format - read-only."""

    def __init__(self, file: AnyFile) -> None:
        """Load and parse Siemens MR RAW (.dat) file."""
        super().__init__(file)
        with self.file as rfile:
            object.__setattr__(self, "fields", load_dat(rfile))

    def get_meta(self) -> MetaData:
        """Return default Flywheel metadata extraction."""
        firstname, lastname = utils.get_patient_name(self)
        timestamp = self.get("PrepareTimestamp")
        meta: dict = {
            "subject.label": self.get("PatientID"),
            "subject.firstname": firstname,
            "subject.lastname": lastname,
            "subject.sex": DAT_SEX_MAP.get(int(self.get("PatientSex") or 3)),
            "session.uid": self.get("StudyInstanceUID"),
            "session.label": utils.get_session_label(self),
            "session.age": utils.get_session_age(self),
            "session.weight": self.get("PatientWeight"),
            "session.timestamp": utils.get_session_timestamp(self) or timestamp,
            "acquisition.uid": utils.get_acquisition_uid(self),
            "acquisition.label": utils.get_acquisition_label(self),
            "acquisition.timestamp": utils.get_acquisition_timestamp(self) or timestamp,
            "file.type": "raw/siemens",  # TODO add core filetype
            "file.name": self.filename,
        }
        return MetaData(meta)


def load_dat(file: BinFile) -> t.Dict[str, t.Any]:
    """Return fields parsed from a Siemens MR RAW (.dat) file."""
    first_line = file.readline()
    if not first_line.strip().endswith(DAT_HEADER):
        raise ValueError(f"Invalid DAT: cannot find header start: {DAT_HEADER!r}")
    fields: dict = {}
    array_key = None
    for line_bytes in file:
        try:
            line = line_bytes.decode()
        except UnicodeDecodeError:
            continue
        dat_field = re.match(DAT_FIELD_RE, line)
        dat_array = re.match(DAT_ARRAY_RE, line)
        dat_value = re.match(DAT_VAL_RE, line)
        if dat_field:
            key = dat_field.group("key")
            value = parse_yaml_value(dat_field.group("value"))
            if value not in ("", None):
                fields.setdefault(key, value)
        elif dat_array:
            array_key = dat_array.group("key")
        elif array_key and dat_value:
            value = parse_yaml_value(dat_value.group("value"))
            if value not in ("", None):
                fields.setdefault(array_key, value)
            array_key = None
    fields = {DAT_KEY_MAP.get(k, k): v for k, v in fields.items()}
    # ensure even simple UIDs like 1.2 are stored as strings
    for key, value in fields.items():
        if key.lower().endswith("uid") and value:
            fields[key] = str(value)
    # convert patient age from float
    if fields.get("PatientAge"):
        fields["PatientAge"] = f"{int(fields['PatientAge'])}Y"
    return fields


#######
# PTD #
#######

PTD_MAGIC_STR = b"LARGE_PET_LM_RAWDATA"
PTD_MAGIC_LEN = len(PTD_MAGIC_STR)
PTD_INT_SIZE = struct.calcsize("i")


class PTDFile(File):
    """Siemens RAW PET / PTD file class.

    PTD is a proprietary file format which has an embedded DICOM dataset:
        <PTD PREAMBLE> <DICOM DATASET> <DICOM SIZE> <MAGIC BYTES>
    This parser peels the wrapping bytes and exposes the embedded DICOM.
    """

    def __init__(self, file: AnyFile, **kwargs) -> None:
        """Read and parse Siemens RAW PET / PTD file, loading the embedded DICOM.

        Args:
            file (str|Path|file): Filepath (str|Path) or open file to read from.
            kwargs: Extra DICOM file keyword arguments.
        """
        super().__init__(file)
        with self.file as rfile:
            dcm_start, dcm_size = get_ptd_dcm_pos(rfile)
            dcm_bytes = rfile.read(dcm_size)
            object.__setattr__(self, "dcm_start", dcm_start)
            object.__setattr__(self, "dcm", DICOM(io.BytesIO(dcm_bytes), **kwargs))

    def __getitem__(self, key: TagType):
        """Get dataelement value by tag/keyword."""
        return self.dcm[key]

    def __setitem__(self, key: TagType, value) -> None:
        """Set dataelement value by tag/keyword."""
        self.dcm[key] = value

    def __delitem__(self, key: TagType) -> None:
        """Delete a dataelement by tag/keyword."""
        del self.dcm[key]

    def __iter__(self):
        """Return dataelement iterator."""
        return iter(self.dcm)

    def __len__(self) -> int:
        """Return the number of elements in the dataset."""
        return len(self.dcm)

    def get_meta(self) -> MetaData:
        """Return the default Flywheel metadata extracted from the PTD."""
        meta = self.dcm.get_meta()
        # TBD path vs meta-based name
        name = self.filename or meta["file.name"] or ""
        meta["file.name"] = re.sub(r"(?i)dcm$", "ptd", name)
        meta["file.type"] = "ptd"  # TBD new core filetype
        return meta

    def save(self, file: AnyFile = None) -> None:
        """Save file."""
        buff = io.BytesIO()
        with self.file as rfile:
            buff.write(rfile.read(self.dcm_start))
        dcm = io.BytesIO()
        self.dcm.save(dcm)
        dcm_bytes = dcm.getvalue()
        buff.write(dcm_bytes)
        buff.write(struct.pack("i", len(dcm_bytes)))
        buff.write(PTD_MAGIC_STR)
        with self.open_dst(file) as wfile:
            wfile.write(buff.getvalue())


def get_ptd_dcm_pos(file: BinFile) -> t.Tuple[int, int]:
    """Return the PTD-embedded DICOM start offset and length."""
    dcm_end = file.seek(-(PTD_MAGIC_LEN + PTD_INT_SIZE), 2)
    dcm_size = struct.unpack("i", file.read(PTD_INT_SIZE))[0]
    magic_str = file.read(PTD_MAGIC_LEN)
    if magic_str != PTD_MAGIC_STR:
        msg = "Invalid PTD magic bytes: {!r} (expected {!r})"
        raise ValueError(msg.format(magic_str, PTD_MAGIC_STR))
    dcm_start = file.seek(dcm_end - dcm_size)
    return dcm_start, dcm_size


#######
# RDA #
#######


RDA_HEADER_START = b">>> Begin of header <<<"
RDA_HEADER_END = b">>> End of header <<<"
RDA_FIELD_RE = r"^(?P<name>\w+)(?P<index>\[[^\]]+\])?:\s*(?P<value>.*?)?\s*$"


class RDAFile(FieldsMixin, File):
    """Siemens MR spectroscopy / RDA file class."""

    def __init__(self, file: AnyFile) -> None:
        """Read and parse a Siemens MR spectroscopy-/ RDA file.

        Args:
            file (str|Path|file): Filepath (str|Path) or open file to read from.
        """
        super().__init__(file)
        with self.file as rfile:
            object.__setattr__(self, "fields", load_rda(rfile))
            object.__setattr__(self, "offset", rfile.tell())

    def get_meta(self) -> MetaData:
        """Return the default Flywheel metadata for the RDA file."""
        firstname, lastname = utils.get_patient_name(self)
        meta: dict = {
            "subject.label": self.get("PatientID"),
            "subject.firstname": firstname,
            "subject.lastname": lastname,
            "subject.sex": self.get("PatientSex"),
            "session.label": utils.get_session_label(self),
            "session.age": utils.get_session_age(self),
            "session.weight": self.get("PatientWeight"),
            "session.timestamp": utils.get_session_timestamp(self),
            "acquisition.label": utils.get_acquisition_label(self),
            "acquisition.timestamp": utils.get_acquisition_timestamp(self),
            "file.type": "spectroscopy",  # TBD new core filetype
            "file.name": self.filename,  # TBD path vs meta-based
        }
        return MetaData(meta)

    def save(self, file: t.Optional[AnyFile] = None) -> None:
        """Save RDA file."""
        bytesio = io.BytesIO()
        bytesio.write(dump_rda(self.fields))
        with self.file as rfile:
            rfile.seek(self.offset)
            bytesio.write(rfile.read())
        with self.open_dst(file) as wfile:
            wfile.write(bytesio.getvalue())


def load_rda(file: BinFile) -> t.Dict[str, t.Any]:
    """Read and parse RDA file header fields."""
    fields: t.Dict[str, t.Any] = {}
    first_line = file.readline()
    if not first_line.startswith(RDA_HEADER_START):
        raise ValueError("Invalid RDA: cannot find header start")
    for line_bytes in file:
        if line_bytes.startswith(RDA_HEADER_END):
            break
        line = line_bytes.decode().strip()
        match = re.match(RDA_FIELD_RE, line)
        if not match:
            raise ValueError(f"Invalid RDA: cannot parse line {line!r}")
        name, index, value = match.groups()
        value = parse_yaml_value(value)
        if index:
            field = fields.setdefault(name, {})
            key = tuple(parse_yaml_value(i) for i in index[1:-1].split(","))
            field[key[0] if len(key) == 1 else key] = value
        else:
            fields[name] = value
    else:
        raise ValueError("Invalid RDA: cannot find header end")
    return fields


def dump_rda(fields: t.Dict[str, t.Any]) -> bytes:
    """Dump RDA header fields to a bytestring."""
    header = io.BytesIO()
    header.write(RDA_HEADER_START + b"\r\n")
    for name, value in fields.items():
        if isinstance(value, dict):
            for key, subval in value.items():
                index = key
                if isinstance(index, tuple):
                    index = ",".join([str(i) for i in key])
                header.write(f"{name}[{index}]: {subval}\r\n".encode())
        else:
            header.write(f"{name}: {value}\r\n".encode())
    header.write(RDA_HEADER_END + b"\r\n")
    return header.getvalue()
