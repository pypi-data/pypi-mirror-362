"""DICOM file Flywheel testing utils."""

import io
import logging
import random
from functools import partial
from pathlib import Path

import pydicom
from faker import Faker
from fw_utils import get_datetime

from .config import UID_PREFIX
from .dicom import DICOM

DCM_BYTE_SIG_OFFSET = 128
DCM_BYTE_SIG = b"DICM"

# sentinel value to skip defaults when using merge_dict
DICT_UNSET = object()

# default tag dict used in create_dcm
DCM_DEFAULT = {
    "SOPClassUID": "1.2.840.10008.5.1.4.1.1.4",  # MR Image Storage
    "SOPInstanceUID": "1.2.3",
    "Modality": "MR",
    "PatientID": "test",
    "StudyInstanceUID": "1",
    "SeriesInstanceUID": "1.2",
}

log = logging.getLogger(__name__)


def generate_dcm(  # noqa: PLR0913 PLR0915
    # TODO support keying off of pre-existing DICOM (str|path|Dataset)
    default_dict: dict | None = None,
    *,
    output_path: str | Path = "./generate_dcm",
    output_name: str = "{sub_no}_{ses_no}_{acq_no}/{SOPInstanceUID}.dcm",
    patients: int | list[dict] | None = None,
    studies: int | list[dict] | None = None,
    series: int | list[dict] | None = None,
    images: int | list[dict] | None = None,
    **default_kw,
) -> None:
    """Generate DICOM files for testing.

    Args:
        default_dict (opt): Default DICOM tags for every instance.
        output_path (opt): Output directory path to write DICOMs to.
        output_name (opt): Filename template for naming DICOM instances.
        patients (opt): Patients to generate (count or list of tag dicts).
        studies (opt): Studies to generate (count or list of tag dicts).
        series (opt): Series to generate (count or list of tag dicts).
        images (opt): Instances to generate (count or list of tag dicts).
        **default_kw (opt): Default DICOM tags as keywords for every instance.
    """

    def auto(name: str, spec: int | list[dict] | None) -> list[dict]:
        err = f"generate_dcm(): invalid arg for {name}: {type(spec)}({spec})"
        if spec is None:
            return [{}]
        if isinstance(spec, int):
            if spec <= 0:  # pragma: no cover
                raise ValueError(err)
            return [{} for _ in range(spec)]
        if isinstance(spec, list):
            return spec
        raise TypeError(err)  # pragma: no cover

    subs = auto("patients", patients)
    sess = auto("studies", studies)
    acqs = auto("series", series)
    imgs = auto("images", images)
    faker = Faker()
    uid_gen = pydicom.uid.generate_uid
    date_gen = faker.date_time_between
    time_gen = partial(faker.time, pattern="%H%M%S")
    dob_gen = partial(faker.date_between, "-75y", "-20y")
    sex_gen = partial(random.choice, ["M", "F"])
    name_gen = {"M": faker.name_male, "F": faker.name_female}
    defaults = (default_dict or {}) | default_kw
    for sub_no, sub in enumerate(subs, start=1):
        sub_prefix = f"{UID_PREFIX}.2.{sub_no}"
        sub = defaults | sub
        sub.setdefault("PatientID", f"subject_{sub_no:03d}")
        sex = sub.setdefault("PatientSex", sex_gen())
        sub.setdefault("PatientName", name_gen.get(sex, faker.name_nonbinary)())
        sub.setdefault("PatientBirthDate", dob_gen().strftime("%Y%m%d"))
        for ses_no, ses in enumerate(sess, start=1):
            ses_prefix = f"{sub_prefix}.{ses_no}"
            ses = sub | ses
            ses.setdefault("StudyInstanceUID", uid_gen(f"{ses_prefix}.0.0."))
            ses.setdefault("StudyDescription", f"session_{ses_no:03d}")
            ses.setdefault("StudyDate", date_gen("-1y").strftime("%Y%m%d"))
            ses.setdefault("StudyTime", time_gen())
            ses.setdefault("AccessionNumber", f"STUDY{ses_no:03d}")
            ses.setdefault("StudyID", ses.get("AccessionNumber"))
            for acq_no, acq in enumerate(acqs, start=1):
                acq_prefix = f"{ses_prefix}.{acq_no}"
                acq = ses | acq
                acq.setdefault("SeriesInstanceUID", uid_gen(f"{acq_prefix}.0."))
                acq.setdefault("SeriesDescription", f"acquisition_{acq_no:03d}")
                acq.setdefault("SeriesNumber", acq_no)
                ses_date = get_datetime(ses.get("StudyDate", "now"))
                acq.setdefault("AcquisitionDate", date_gen(ses_date).strftime("%Y%m%d"))
                acq.setdefault("AcquisitionTime", time_gen())
                for img_no, img in enumerate(imgs, start=1):
                    img_prefix = f"{acq_prefix}.{img_no}."
                    img = acq | img
                    img.setdefault("Modality", "MR")
                    img.setdefault("InstanceNumber", img_no)
                    img.setdefault("SOPClassUID", "1.2.840.10008.5.1.4.1.1.4")
                    img.setdefault("SOPInstanceUID", uid_gen(img_prefix))
                    path = Path(output_path) / output_name.format(**locals(), **img)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(create_dcm_as_bytes(**img).getvalue())


def create_dcm(file=None, preamble=None, file_meta=None, **dcmdict):
    """Create a dataset and return it loaded as an fw_file.dicom.DICOM."""
    dcmdict = merge_dict(dcmdict, DCM_DEFAULT)
    dcm = create_dcm_as_bytes(dcmdict, preamble=preamble, file_meta=file_meta)
    if file:
        Path(file).write_bytes(dcm.getvalue())
    return DICOM(file or dcm)


def create_dcm_as_bytes(
    dcmdict: dict | None = None,
    *,
    preamble: bytes | None = None,
    file_meta: dict | None = None,
    **kw,
) -> io.BytesIO:
    """Create and return a DICOM file as BytesIO object from a tag dict."""
    dcmdict = dcmdict or {}
    file = io.BytesIO()
    dataset = pydicom.FileDataset(file, create_dataset(dcmdict | kw))
    dataset.preamble = preamble or b"\x00" * 128
    dataset.file_meta = pydicom.FileMetaDataset()
    update_dataset(dataset.file_meta, file_meta)
    pydicom.dcmwrite(file, dataset, enforce_file_format=not bool(file_meta))
    file.seek(0)
    return file


def create_dataset(
    dcmdict: dict | None = None,
    **kw,
) -> pydicom.Dataset:
    """Create and return a pydicom.Dataset from a simple tag dictionary."""
    dcmdict = dcmdict or {}
    dataset = pydicom.Dataset()
    update_dataset(dataset, dcmdict | kw)
    return dataset


def update_dataset(dataset: pydicom.Dataset, dcmdict: dict) -> None:
    """Add dataelements to a dataset from the given tag dictionary."""
    dcmdict = dcmdict or {}
    for key, value in dcmdict.items():
        # if value is a list/tuple, it's expected to be a (VR,value) pair
        if isinstance(value, (list, tuple)):
            VR, value = value
        # otherwise it's just the value, so get the VR from the datadict
        else:
            VR = pydicom.datadict.dictionary_VR(key)
        if VR == "SQ":
            value = [create_dataset(v) for v in value]
        dataset.add_new(key, VR, value)


def merge_dict(custom: dict, default: dict) -> dict:
    """Merge a custom dict onto some defaults."""
    merged = default | custom
    return {k: v for k, v in merged.items() if v is not DICT_UNSET}
