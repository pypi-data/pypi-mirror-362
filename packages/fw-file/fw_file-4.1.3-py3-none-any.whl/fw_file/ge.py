"""GE MR RAW / PFile (PNNNNN.7) file format."""

import struct
import typing as t
from datetime import datetime, timedelta, timezone

from fw_meta import MetaData
from fw_utils import AttrDict

from .base import AnyFile, FieldsMixin, File
from .dicom.utils import parse_person_name

# num of bytes to read into memory (must cover all parsed offsets)
HEADER_SIZE = 256 << 10  # 256 KB

# possible logo (~ magic bytes) variants
PFILE_LOGOS = {"GE_MED_NMR", "INVALIDNMR"}


class PFile(FieldsMixin, File):
    """GE MR RAW / PFile (PNNNNN.7) file format."""

    def __init__(self, file: AnyFile) -> None:
        """Read and parse a PFile, supporting only a subset of the fields.

        Args:
            file (str|Path|file): Filepath (str|Path) or open file to read from.
        """
        super().__init__(file)
        with self.file as rfile:
            # read the first 256K that covers all parsed fields
            header = rfile.read(HEADER_SIZE)
            # parse pfile version number (float) from the first 4 bytes
            version: float = round(unpack(header, 0, "f"), 3)
            if version not in VERSION_OFFSETS:
                raise ValueError(f"Invalid PFile or unsupported version: {version}")
            # parse known fields with the offsets for the version
            offsets = VERSION_OFFSETS[version]
            fields = {}
            for name, (offset, fmt) in offsets.items():
                value = unpack(header, offset, fmt)
                fields[name] = value
            # validate pfile logo / magic bytes
            if fields["logo"] not in PFILE_LOGOS:
                raise ValueError(f"Invalid PFile logo: {fields['logo']!r}")
        object.__setattr__(self, "header", header)
        object.__setattr__(self, "version", version)
        object.__setattr__(self, "fields", fields)

    def get_meta(self) -> MetaData:
        """Return the default Flywheel metadata of the PFile."""
        firstname, lastname = parse_person_name(self.PatientName or "")
        timestamp = self.get_acquisition_timestamp()
        meta: dict = {
            "subject.label": self.PatientID,
            "subject.firstname": firstname,
            "subject.lastname": lastname,
            "session.uid": self.StudyInstanceUID,
            "session.timestamp": timestamp,
            "acquisition.uid": f"{self.SeriesInstanceUID}_{self.AcquisitionNumber}",
            "acquisition.label": self.SeriesDescription,
            "acquisition.timestamp": timestamp,
            "file.type": "pfile",
            "file.name": self.filename,
        }
        return MetaData(meta)

    @property
    def ge_physio_match(self) -> AttrDict:
        """Return the metadata needed for matching GE physio filenames to."""
        psn = self.PulseSequenceName
        start = self.get_acquisition_timestamp()
        duration = self.AcquisitionDuration
        return AttrDict(psn=psn.lower(), end=start + timedelta(seconds=duration))

    def get_acquisition_timestamp(self) -> datetime:
        """Return the acquisition timestamp."""
        if self.AcquisitionDateTime > 0:
            return datetime.fromtimestamp(self.AcquisitionDateTime, timezone.utc)
        month, day, year = [int(i) for i in self.AcquisitionDate.split("/")]
        hour, minute = [int(i) for i in self.AcquisitionTime.split(":")]
        year += 1900  # GE epoch begins in 1900
        return datetime(year, month, day, hour, minute)

    def save(self, file: AnyFile = None) -> None:
        """Save file."""
        with self.file as rfile:
            rfile.seek(HEADER_SIZE)
            epilogue = rfile.read()
        with self.open_dst(file) as wfile:
            tell = wfile.write(pack(self.version, "f"))
            for name, (offset, fmt) in VERSION_OFFSETS[self.version].items():
                if offset > tell:
                    tell += wfile.write(self.header[tell:offset])
                if not self.get(name):
                    size = struct.calcsize("32s" if fmt == "uid" else fmt)
                    tell += wfile.write(bytes(size))
                    continue
                tell += wfile.write(pack(self[name], fmt))
            wfile.write(epilogue)


def unpack(raw: bytes, offset: int, fmt: str):
    """Return field parsed from the raw bytes using the offset and format."""
    uid = fmt == "uid"
    fmt = "32s" if uid else fmt
    start, end = offset, offset + struct.calcsize(fmt)
    value = struct.unpack(fmt, raw[start:end])[0]
    if uid:
        # see: https://en.wikipedia.org/wiki/Binary-coded_decimal
        components = [
            str(byte - 1) if byte < 11 else "."
            for pair in [(b >> 4, b & 15) for b in value]
            for byte in pair
            if byte > 0
        ]
        value = "".join(components)
    if isinstance(value, bytes):
        value = value.split(b"\x00", 1)[0].decode()
    return value


def pack(value, fmt: str) -> bytes:
    """Return field value packed in raw bytes format."""
    uid = fmt == "uid"
    fmt = "32s" if uid else fmt
    if uid:
        bs = bytes(11 if c == "." else int(c) + 1 for c in value)
        bi = iter(bs.ljust(32, b"\x00"))
        value = bytes(b1 << 4 | b2 for b1, b2 in zip(bi, bi))
    if isinstance(value, str):
        value = value.encode()
    return struct.pack(fmt, value)


# PFile {version: field_offsets} map
# Adding support for a new version:
#   1. Duplicate the closest version within the dict
#   2. Set the key to the version number being added
#   3. Update field offsets (ask Michael Perry / Gunnar Shaefer for more)
# TODO consider de-duplicating (not declaring identical sections again)
# TODO add forwards-compatibility (new versions don't seem to change at all)
VERSION_OFFSETS: t.Dict[float, t.Dict[str, t.Tuple[int, str]]] = {
    30.0: {
        "AcquisitionDate": (92, "10s"),  # char rdb_hdr_scan_date
        "AcquisitionTime": (102, "8s"),  # char rdb_hdr_scan_time
        "logo": (110, "10s"),  # char rdb_hdr_logo
        "StudyID": (202548, "H"),  # ushort ex_no
        "StudyInstanceUID": (203280, "uid"),  # char*32 study_uid
        "PatientName": (203376, "65s"),  # char*65 patnameff
        "PatientID": (203441, "65s"),  # char*65 patidff
        "AccessionNumber": (203506, "17s"),  # char*17 reqnumff
        "PatientsBirthDate": (203523, "9s"),  # char*9 dateofbirth
        "SeriesNumber": (204548, "h"),  # int se_no
        "SeriesDescription": (204794, "65s"),  # char se_desc
        "SeriesInstanceUID": (204957, "uid"),  # char series_uid
        "AcquisitionDuration": (206684, "f"),  # float sctime
        "AcquisitionDateTime": (207420, "i"),  # int im_datetime
        "AcquisitionNumber": (207866, "h"),  # short scanactno
        "PulseSequenceName": (208004, "33s"),  # char psdname
    },
    28.003: {
        "AcquisitionDate": (92, "10s"),
        "AcquisitionTime": (102, "8s"),
        "logo": (110, "10s"),
        "StudyID": (202548, "H"),
        "StudyInstanceUID": (203280, "uid"),
        "PatientName": (203376, "65s"),
        "PatientID": (203441, "65s"),
        "AccessionNumber": (203506, "17s"),
        "PatientsBirthDate": (203523, "9s"),
        "SeriesNumber": (204548, "h"),
        "SeriesDescription": (204794, "65s"),
        "SeriesInstanceUID": (204957, "uid"),
        "AcquisitionDuration": (206684, "f"),
        "AcquisitionDateTime": (207420, "i"),
        "AcquisitionNumber": (207866, "h"),
        "PulseSequenceName": (208004, "33s"),
    },
    28.002: {
        "AcquisitionDate": (92, "10s"),
        "AcquisitionTime": (102, "8s"),
        "logo": (110, "10s"),
        "StudyID": (202548, "H"),
        "StudyInstanceUID": (203280, "uid"),
        "PatientName": (203376, "65s"),
        "PatientID": (203441, "65s"),
        "AccessionNumber": (203506, "17s"),
        "PatientsBirthDate": (203523, "9s"),
        "SeriesNumber": (204548, "h"),
        "SeriesDescription": (204794, "65s"),
        "SeriesInstanceUID": (204957, "uid"),
        "AcquisitionDuration": (206684, "f"),
        "AcquisitionDateTime": (207420, "i"),
        "AcquisitionNumber": (207866, "h"),
        "PulseSequenceName": (208004, "33s"),
    },
    27.001: {
        "AcquisitionDate": (92, "10s"),
        "AcquisitionTime": (102, "8s"),
        "logo": (110, "10s"),
        "StudyID": (202548, "H"),
        "StudyInstanceUID": (203280, "uid"),
        "PatientName": (203376, "65s"),
        "PatientID": (203441, "65s"),
        "AccessionNumber": (203506, "17s"),
        "PatientsBirthDate": (203523, "9s"),
        "SeriesNumber": (204548, "h"),
        "SeriesDescription": (204794, "65s"),
        "SeriesInstanceUID": (204957, "uid"),
        "AcquisitionDuration": (206684, "f"),
        "AcquisitionDateTime": (207420, "i"),
        "AcquisitionNumber": (207866, "h"),
        "PulseSequenceName": (208004, "33s"),
    },
    27.0: {
        "AcquisitionDate": (92, "10s"),
        "AcquisitionTime": (102, "8s"),
        "logo": (110, "10s"),
        "StudyID": (194356, "H"),
        "StudyInstanceUID": (195088, "uid"),
        "PatientName": (195184, "65s"),
        "PatientID": (195249, "65s"),
        "AccessionNumber": (195314, "17s"),
        "PatientsBirthDate": (195331, "9s"),
        "SeriesNumber": (196356, "h"),
        "SeriesDescription": (196602, "65s"),
        "SeriesInstanceUID": (196765, "uid"),
        "AcquisitionDuration": (198492, "f"),
        "AcquisitionDateTime": (199228, "i"),
        "AcquisitionNumber": (199674, "h"),
        "PulseSequenceName": (199812, "33s"),
    },
    26.002: {
        "AcquisitionDate": (92, "10s"),
        "AcquisitionTime": (102, "8s"),
        "logo": (110, "10s"),
        "StudyID": (194356, "H"),
        "StudyInstanceUID": (195088, "uid"),
        "PatientName": (195184, "65s"),
        "PatientID": (195249, "65s"),
        "AccessionNumber": (195314, "17s"),
        "PatientsBirthDate": (195331, "9s"),
        "SeriesNumber": (196356, "h"),
        "SeriesDescription": (196602, "65s"),
        "SeriesInstanceUID": (196765, "uid"),
        "AcquisitionDuration": (198492, "f"),
        "AcquisitionDateTime": (199228, "i"),
        "AcquisitionNumber": (199674, "h"),
        "PulseSequenceName": (199812, "33s"),
    },
    24.0: {
        "AcquisitionDate": (16, "10s"),
        "AcquisitionTime": (26, "8s"),
        "logo": (34, "10s"),
        "StudyID": (143516, "H"),
        "StudyInstanceUID": (144248, "uid"),
        "PatientName": (144344, "65s"),
        "PatientID": (144409, "65s"),
        "AccessionNumber": (144474, "17s"),
        "PatientsBirthDate": (144491, "9s"),
        "SeriesNumber": (145622, "h"),
        "SeriesDescription": (145762, "65s"),
        "SeriesInstanceUID": (145875, "uid"),
        "AcquisitionDuration": (147652, "f"),
        "AcquisitionDateTime": (148388, "i"),
        "AcquisitionNumber": (148834, "h"),
        "PulseSequenceName": (148972, "33s"),
    },
    21.001: {
        "AcquisitionDate": (16, "10s"),
        "AcquisitionTime": (26, "8s"),
        "logo": (34, "10s"),
        "StudyID": (144064, "H"),
        "StudyInstanceUID": (144788, "uid"),
        "PatientName": (144884, "65s"),
        "PatientID": (144949, "65s"),
        "AccessionNumber": (145014, "17s"),
        "PatientsBirthDate": (145031, "9s"),
        "SeriesNumber": (146170, "h"),
        "SeriesDescription": (146310, "65s"),
        "SeriesInstanceUID": (146423, "uid"),
        "AcquisitionDuration": (148200, "f"),
        "AcquisitionDateTime": (148936, "i"),
        "AcquisitionNumber": (149382, "h"),
        "PulseSequenceName": (149520, "33s"),
    },
    20.007: {
        "AcquisitionDate": (16, "10s"),
        "AcquisitionTime": (26, "8s"),
        "logo": (34, "10s"),
        "StudyID": (143516, "H"),
        "StudyInstanceUID": (144248, "uid"),
        "PatientName": (144344, "65s"),
        "PatientID": (144409, "65s"),
        "AccessionNumber": (144474, "17s"),
        "PatientsBirthDate": (144491, "9s"),
        "SeriesNumber": (145622, "h"),
        "SeriesDescription": (145762, "65s"),
        "SeriesInstanceUID": (145875, "uid"),
        "AcquisitionDuration": (147652, "f"),
        "AcquisitionDateTime": (148388, "i"),
        "AcquisitionNumber": (148834, "h"),
        "PulseSequenceName": (148972, "33s"),
    },
    20.006: {
        "AcquisitionDate": (16, "10s"),
        "AcquisitionTime": (26, "8s"),
        "logo": (34, "10s"),
        "StudyID": (143516, "H"),
        "StudyInstanceUID": (144240, "uid"),
        "PatientName": (144336, "65s"),
        "PatientID": (144401, "65s"),
        "AccessionNumber": (144466, "17s"),
        "PatientsBirthDate": (144483, "9s"),
        "SeriesNumber": (145622, "h"),
        "SeriesDescription": (145762, "65s"),
        "SeriesInstanceUID": (145875, "uid"),
        "AcquisitionDuration": (147652, "f"),
        "AcquisitionDateTime": (148388, "i"),
        "AcquisitionNumber": (148834, "h"),
        "PulseSequenceName": (148972, "33s"),
    },
    11.0: {
        "AcquisitionDate": (16, "10s"),
        "AcquisitionTime": (26, "8s"),
        "logo": (34, "10s"),
        "StudyID": (61576, "H"),
        "StudyInstanceUID": (61966, "uid"),
        "PatientName": (62062, "65s"),
        "PatientID": (62127, "65s"),
        "AccessionNumber": (62192, "17s"),
        "PatientsBirthDate": (62209, "9s"),
        "SeriesNumber": (62710, "h"),
        "SeriesDescription": (62786, "65s"),
        "SeriesInstanceUID": (62899, "uid"),
        "AcquisitionDuration": (64544, "f"),
        "AcquisitionDateTime": (65016, "i"),
        "AcquisitionNumber": (65328, "h"),
        "PulseSequenceName": (65374, "33s"),
    },
}
