"""Base class for all EEG filetypes supported by MNE."""

import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

import mne
from fw_meta import MetaData
from fw_utils import AnyPath

from .base import FieldsMixin, File, ReadOnly
from .utils import birthdate_to_age

MNE_SEX_MAP = {0: "O", 1: "M", 2: "F"}

EXT_TO_FMT = {
    ".edf": "edf",
    ".bdf": "bdf",
    ".set": "eeglab",
    ".vhdr": "brainvision",
    ".ahdr": "brainvision",
}


class MneEeg(FieldsMixin, File):
    """Base class for EEG ingest that detects file format.

    Supports the following filetypes: BrainVision, EDF, EDF+, BDF, BDF+, EEGLAB

    All keys of the mne.Info metadata dictionary are exposed as attributes of this
    class. Each of these attributes returns None if unset

    `subject_info` is the only attribute of this class that should be set directly

    All other modifications/additions to the mne.Info dictionary should be performed
    through method calls on the mne.io.Raw object

    The mne.io.Raw object containing the parsed EEG file is accessed with the `raw'
    attribute
    """

    def __init__(self, file: AnyPath):
        """Load and parse EEG files".

        Args:
            file (str|Path): Filepath of supported type: .edf, .bdf, .set, .vhdr
        """
        super().__init__(file)
        try:
            object.__getattribute__(self, "_fmt")
        except AttributeError:
            object.__setattr__(self, "_fmt", get_fmt(Path(file)))
        if self._fmt == "bdf" and self.__class__.__name__ == "MneEeg":
            raise RuntimeError("For BDF/BDF+ files, use the 'BDF' class.")
        object.__setattr__(self, "raw", mne.io.read_raw(file, verbose=40))
        object.__setattr__(self, "fields", self.raw.info)

    @property
    def file_format(self) -> str:
        """Format of underlying EEG file.

        Possible values: 'edf', 'bdf', 'eeglab', 'brainvision'.
        """
        return self._fmt

    def get_meta(self) -> MetaData:
        """Return the default Flywheel metadata."""
        meta: dict = {"file.type": "eeg", "file.name": self.filename}

        if subj := self.subject_info:
            if self._fmt in ["edf", "bdf"]:
                # EDF/BDF standard dictates that unknown subfields are indicated by
                # the letter 'X'
                subj = {k: (None if v == "X" else v) for (k, v) in subj.items()}
            subj_info: dict = {
                "subject.label": subj.get("his_id"),
                "subject.firstname": subj.get("first_name"),
                "subject.lastname": subj.get("last_name"),
                "session.weight": subj.get("weight"),
            }
            if self.meas_date and subj.get("birthday"):
                birthday = subj.get("birthday")
                # Handle birthday as a tuple (year, month, day)
                if isinstance(birthday, tuple) and len(birthday) == 3:
                    birthday = datetime(*birthday).date()
                subj_info.update(
                    {"session.age": birthdate_to_age(birthday, self.meas_date)}
                )
            if subj.get("sex"):
                subj_info.update({"subject.sex": MNE_SEX_MAP[subj.get("sex")]})
            meta.update(subj_info)

        if self.meas_date:
            meta.update({"session.timestamp": self.meas_date})

        return MetaData(clear_empty_keys(meta))

    def save(self, file: AnyPath = None, overwrite: bool = False) -> None:  # type: ignore
        """Save either to specified filepath or to original path of eeg file."""
        f = file if file else self.filepath
        self.raw.info = self.fields
        mne.export.export_raw(str(f), self.raw, overwrite=overwrite, fmt=self._fmt)


class BrainVision(MneEeg):
    """EEG ingest class for BrainVision files."""

    def __init__(self, file: AnyPath):
        """Load and parse BrainVision files".

        Args:
            file (str|Path): Filepath to an BrainVision header file (.vhdr). The
            corresponding marker (.vmrk) and data (.eeg) files must be present in
            the same directory as the header.
        """
        object.__setattr__(self, "_fmt", "brainvision")
        super().__init__(file)

    @classmethod
    def from_zip(cls, archive: AnyPath) -> "BrainVision":
        """Return BrainVision from a ZIP archive.

        Args:
            archive (str|Path): The ZIP archive path or readable to extract
                into a temporary directory and read all files from.
        """
        tempdir = tempfile.mkdtemp()
        with zipfile.ZipFile(archive, mode="r") as zfile:
            zfile.extractall(tempdir)
        # Unzip creates a real header file and a hidden (dotted) header file
        # Exclude hidden file from glob
        header_path = list(Path(tempdir).glob("**/[!.]*.vhdr"))[0]
        bv = cls(header_path)
        shutil.rmtree(tempdir)
        return bv


class EDF(MneEeg):
    """EEG ingest class for EDF, EDF+ files."""

    def __init__(self, file: AnyPath):
        """Load and parse EDF, EDF+ files".

        Args:
            file (str|Path): Filepath to an EDF file (.edf)
        """
        object.__setattr__(self, "_fmt", "edf")
        super().__init__(file)


class EEGLAB(MneEeg):
    """EEG ingest class for EEGLAB files."""

    def __init__(self, file: AnyPath):
        """Load and parse EEGLAB files".

        Args:
            file (str|Path): Filepath to a EEGLAB file (.set). If data is contained in
            an additional .fdt file, it must be in the same directory as the .set file.
        """
        object.__setattr__(self, "_fmt", "eeglab")
        super().__init__(file)

    @classmethod
    def from_zip(cls, archive: AnyPath) -> "EEGLAB":
        """Return EEGLAB from a ZIP archive.

        Args:
            archive (str|Path): The ZIP archive path or readable to extract
                into a temporary directory and read all files from.
        """
        tempdir = tempfile.mkdtemp()
        with zipfile.ZipFile(archive, mode="r") as zfile:
            zfile.extractall(tempdir)
        # Unzip creates a real set file and a hidden (dotted) set file
        # Exclude hidden file from glob
        set_path = list(Path(tempdir).glob("**/[!.]*.set"))[0]
        eeglab = cls(set_path)
        shutil.rmtree(tempdir)
        return eeglab


class BDF(ReadOnly, MneEeg):
    """EEG ingest class for BDF, BDF+ files."""

    def __init__(self, file: AnyPath):
        """Load and parse BDF, BDF+ files".

        Args:
            file (str|Path): Filepath to a BDF file (.bdf)
        """
        object.__setattr__(self, "_fmt", "bdf")
        super().__init__(file)

    def save(self, file: AnyPath = None, overwrite: bool = False) -> None:  # type: ignore
        """Overwrite MneEeg save method as BDF is read-only."""
        raise TypeError(f"{self.__class__.__name__} is read-only")


def clear_empty_keys(d: dict) -> dict:
    """Returns dictionary with keys removed that correspond to value of None."""
    return {key: value for (key, value) in d.items() if value not in (None, "")}


def get_fmt(p: Path) -> str:
    """Get EEG format given file extension."""
    return EXT_TO_FMT[p.suffix]
