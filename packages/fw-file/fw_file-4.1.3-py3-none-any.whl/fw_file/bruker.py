"""Bruker ParaVision file format - read only (subject/acqp/method files)."""

import re
import typing as t
from datetime import datetime

from fw_meta import MetaData
from fw_utils import BinFile, get_datetime

from .base import AnyFile, FieldsMixin, File, ReadOnly

ARRAY_RE = re.compile(r"\( \d+(, \d+)* \)")
VERSION_RE = re.compile(r"(PV|ParaVision) ?(?P<ver>\d+(\.\d+)+)")


class ParaVision(ReadOnly, FieldsMixin, File):
    """Bruker ParaVision file class."""

    def __init__(self, file: AnyFile) -> None:
        """Read and parse a Bruker ParaVision file.

        Args:
            file (str|Path|file): Filepath (str|Path) or open file to read from.
        """
        super().__init__(file)
        with self.file as rfile:
            object.__setattr__(self, "fields", load_paravision(rfile))

    def get_meta(self) -> MetaData:
        """Return the default Flywheel metadata for a ParaVision file."""
        study_name = self.get("subject_study_name", "")
        session_ts = get_timestamp(
            self.get("subject_study_date")  # pv360 and up
            or self.get("subject_abs_date")  # pv7 and down
            or ""
        )
        session_label_parts = []
        if study_name:
            session_label_parts.append(study_name)
        if session_ts:
            session_label_parts.append(session_ts.strftime("%Y%m%d%H%M%S"))
        session_label = " - ".join(session_label_parts)
        acq_ts = get_timestamp(self.get("acq_abs_time", ""))
        meta = {
            "subject.label": self.get("subject_id"),
            "subject.sex": self.get("subject_sex"),
            "session.uid": self.get("subject_study_instance_uid"),
            "session.label": session_label,
            "session.timestamp": session_ts,
            "acquisition.label": self.get("acq_protocol_name"),
            "acquisition.timestamp": acq_ts,
            "file.type": "ParaVision",
            "file.name": self.filename,
        }
        return MetaData(meta)


def load_paravision(file: BinFile) -> t.Dict[str, t.Any]:
    """Parse ParaVision parameters file as a dictionary."""
    fields: t.Dict[str, t.Any] = {}
    key = None
    for line_bytes in file:
        line = line_bytes.decode()
        if not fields.get("version"):
            match = VERSION_RE.search(line)
            if match:
                fields["version"] = match.group("ver")
        if line.startswith("$$"):
            continue
        if line.startswith("##"):
            key, _, value = line.partition("=")
            key = key.lstrip("##$").lower()
            if ARRAY_RE.match(value):
                value = ""
        else:
            value = line
        if key:
            # strip starting/ending chars
            value = value.strip(" <>\n")
            # keep a newline if value ends with an escape
            if value.endswith("\\"):
                value = value[:-1] + "\n"
            fields[key] = fields.get(key, "") + value

    return fields


def get_timestamp(value: str) -> t.Optional[datetime]:
    """Return iso timestamp from bruker epoch value."""
    abs_time, *_ = value.strip("()").partition(",")
    if not abs_time:
        return None
    return get_datetime(int(abs_time))
