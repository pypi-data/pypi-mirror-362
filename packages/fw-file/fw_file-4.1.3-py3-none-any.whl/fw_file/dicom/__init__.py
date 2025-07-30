"""dicom module."""

from pydicom import dataset

from .config import get_config
from .dcmdict import load_dcmdict, load_private_dictionaries
from .dicom import DICOM, TagType, get_private_tag
from .reader import ReadContext
from .series import DICOMCollection, DICOMSeries, build_dicom_tree
from .utils import generate_uid

__all__ = [
    "DICOM",
    "DICOMCollection",
    "DICOMSeries",
    "TagType",
    "build_dicom_tree",
    "generate_uid",
    "get_config",
    "load_dcmdict",
    "ReadContext",
    "get_private_tag",
]

# Extend pydicom private dict (with shipped extras and DCMDICTPATH if set)
load_private_dictionaries()

# Patch (wrap) Dataset.__getitem__ to always use a read context
orig_dataset_getitem = dataset.Dataset.__getitem__


def dataset_getitem_with_context(self, key):
    """Dataset __getitem__ method with ReadContext."""
    with getattr(self, "read_context", ReadContext.from_callback_kwargs()):
        return orig_dataset_getitem(self, key)


dataset.Dataset.__getitem__ = dataset_getitem_with_context  # type: ignore
