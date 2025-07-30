"""DICOM config module."""

import functools
import importlib
import re
import typing as t
from collections.abc import MutableSequence
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydicom import config as pydicom_config
from pydicom.dataelem import RawDataElement
from pydicom.dataset import Dataset
from pydicom.hooks import hooks
from pydicom.values import convert_value

from .. import __version__

__all__ = [
    "get_config",
    "IMPLEMENTATION_CLASS_UID",
    "IMPLEMENTATION_VERSION_NAME",
    "UID_ROOT",
    "UID_PREFIX",
]

READER: str = "ReadContext"


# Flywheel DICOM UID Management Plan:
# https://docs.google.com/document/d/1HcMcWBrDsYIFOkMgGL8W7Hzt7I2tl4UbeC40R5HH99A
# UID root for ANSI registered numeric organization name 114570 (Flywheel)
UID_ROOT = "2.16.840.1.114570"
# UID prefix and version of product fw-file
UID_PREFIX = f"{UID_ROOT}.4"
VERSION = re.split(r"[^\d]+", __version__)

# fw-file (0002,0012) ImplementationClassUID
IMPLEMENTATION_CLASS_UID: str = f"{UID_PREFIX}.1.{'.'.join(VERSION)}"
# fw-file (0002,0013) ImplementationVersionName
IMPLEMENTATION_VERSION_NAME: str = f"FWFILE_{'_'.join(VERSION)}"


@functools.lru_cache()
def import_func(func_path: str) -> t.Callable:
    """Return function imported from a fully qualified name."""
    try:
        module_name, func_name = func_path.rsplit(".", maxsplit=1)
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
    except (ValueError, ImportError, AttributeError) as exc:
        msg = f"Cannot import fixer {func_path!r} ({exc})"
        raise ValueError(msg) from exc
    assert callable(func), f"{func_path} is not callable"
    return func


class DICOMConfig(BaseSettings):
    """DICOM config."""

    model_config = SettingsConfigDict(
        env_prefix="FW_DCM_",
        validate_assignment=True,
    )

    # data element loader / fixer config
    fix_VR_mismatch: bool = False
    fix_VR_mismatch_with_VRs: t.List[str] = ["PN", "DS", "IS"]
    track: bool = False

    # pydicom.config values
    # 0==IGNORE, 1==WARN, 2==RAISE
    reading_validation_mode: int = 1
    writing_validation_mode: int = 1

    @field_validator("reading_validation_mode")
    def sync_rvm(cls, value) -> int:
        """Sync pydicom_config when config is changed."""
        pydicom_config.settings.reading_validation_mode = value
        return value

    @field_validator("writing_validation_mode")
    def sync_wvm(cls, value) -> int:
        """Sync pydicom_config when config is changed."""
        pydicom_config.settings.writing_validation_mode = value
        return value

    # read-only mode
    read_only: bool = False

    # dicom standard
    standard_path: Path = Path(__file__).parent / "standard"
    standard_rev: str = "2024e"

    # If standard_rev is changed after get_standard has been
    # called, the cache needs to be cleared, otherwise it may
    # try to use the previously cached standard.
    @field_validator("standard_rev")
    def clear_on_rev_change(cls, value) -> str:
        """Clears get_standard cache on standard_rev change."""
        from .validation import get_standard  # noqa: PLC0415

        get_standard.cache_clear()
        return value

    # Previously, fixers were together in `raw_elem_fixers`,
    # but as of pydicom 3.0.x, fixers are categorized into
    # VR and value fixers.
    raw_VR_fixers: t.List[t.Union[str, t.Callable]] = [
        "fw_file.dicom.fixers.tag_specific_fixer",
        "fw_file.dicom.fixers.apply_dictionary_VR",
    ]
    raw_value_fixers: t.List[t.Union[str, t.Callable]] = [
        "fw_file.dicom.fixers.replace_backslash_in_VM1_str",
        "fw_file.dicom.fixers.convert_exception_fixer",
        "fw_file.dicom.fixers.LUT_descriptor_fixer",
    ]

    @field_validator("raw_VR_fixers")
    @classmethod
    def check_VR_fixers(cls, v):
        """Resolve string/functions for VR fixers, import if str, register callback."""
        callbacks = []
        for val in v:
            fn = val
            if isinstance(val, str):
                fn = import_func(val)
            callbacks.append(fn)
        hooks.raw_element_kwargs["raw_VR_fixers"] = callbacks
        hooks.register_callback("raw_element_vr", chain_VR_fixers)
        return callbacks

    @field_validator("raw_value_fixers")
    @classmethod
    def check_value_fixers(cls, v):
        """Resolve string/functions for value fixers, import if str, register callback."""
        callbacks = []
        for val in v:
            fn = val
            if isinstance(val, str):
                fn = import_func(val)
            callbacks.append(fn)
        hooks.raw_element_kwargs["raw_value_fixers"] = callbacks
        hooks.register_callback("raw_element_value", chain_value_fixers)
        return callbacks

    def add_fixers(
        self,
        fixers: t.Union[t.List[t.Union[t.Callable, str]], t.Callable, str],
        fix_type: str,
        index: t.Optional[int] = None,
    ) -> None:
        """Helper function to add one or more raw element fixers.

        Args:
            fixers (List, Callable, str): List or single function to add, can
                either be specified as the actual function or a string
                representing its import path.
            fix_type (str): "VR" or "value", depending on which is fixed.
            index (int): Optional index at which to add the fixer(s)
        """
        if fix_type == "VR":
            fix_list = self.raw_VR_fixers
        elif fix_type == "value":
            fix_list = self.raw_value_fixers
        else:
            raise ValueError(f"fix_type must be either 'VR' or 'value', not {fix_type}")
        if not isinstance(fixers, list):
            fixers = [fixers]
        add = [import_func(fn) if isinstance(fn, str) else fn for fn in fixers]
        if index:
            fix_list[index:index] = add
            return
        fix_list.extend(add)
        return

    def remove_fixers(self, fixers: t.Union[t.List[str], str]) -> None:
        """Helper function to remove one or more raw_elem_fixers.

        Args:
            fixers (List, str): List or single string representing the name of
                the function to remove.  You don't need to specify the full
                import path, just the name of the function.
        """
        if not isinstance(fixers, list):
            fixers = [fixers]
        for to_remove in fixers:
            self.raw_VR_fixers = [
                fn
                for fn in self.raw_VR_fixers
                if fn.__name__ != to_remove  # type: ignore
            ]
            self.raw_value_fixers = [
                fn
                for fn in self.raw_value_fixers
                if fn.__name__ != to_remove  # type: ignore
            ]

    def list_fixers(self) -> t.List[str]:
        """Helper to list name and order of all enabled fixers."""
        return [fn.__name__ for fn in self.raw_VR_fixers + self.raw_value_fixers]  # type: ignore

    # allow private tag access without specifying private creator like dcm["0019xx10"]
    # when enabled dataset/private dict will be used to figure out the private creator
    implicit_creator: bool = False

    # num of instances (with local paths) to keep loaded in memory in collections
    instance_cache_size: int = 10000


@functools.lru_cache(maxsize=None)
def get_config() -> DICOMConfig:
    """Return DICOMConfig object loaded from envvars (cached / singleton)."""
    return DICOMConfig()


def chain_VR_fixers(
    raw: RawDataElement,
    data: dict[str, t.Any],
    *,
    encoding: str | MutableSequence[str] | None = None,
    ds: Dataset | None = None,
    **kwargs: t.Any,
) -> None:
    """Initializes ReadContext and iterates through all enabled VR fixers.

    After all VR fixers are completed, updates the ReadContext and data["VR"].
    """
    if read_ctx := kwargs.get(READER):
        if read_ctx.encoding is None:
            read_ctx.encoding = encoding
        raw = read_ctx.track(raw)
    if fixers := kwargs.get("raw_VR_fixers"):
        for fx in fixers:
            raw = fx(raw, encoding=encoding, dataset=ds, **hooks.raw_element_kwargs)

    if read_ctx:
        read_ctx.update(raw)

    data["VR"] = t.cast(str, raw.VR)


def chain_value_fixers(
    raw: RawDataElement,
    data: dict[str, t.Any],
    *,
    encoding: str | MutableSequence[str] | None = None,
    ds: Dataset | None = None,
    **kwargs: t.Any,
) -> None:
    """Initializes ReadContext and iterates through all enabled value fixers.

    If VR was changed by a VR fixer, updates the RawDataElement to match before
    iterating through value fixers. After all VR fixers are completed, updates the
    ReadContext as well as data["VR"] and data["value"].
    """
    if read_ctx := kwargs.get(READER):
        if read_ctx.encoding is None:
            read_ctx.encoding = encoding
        raw = read_ctx.track(raw)

    if VR := data.get("VR"):
        # The original fixer method assumes that the raw is changing and the updated
        # version is always being passed to the next fixer, but because the hooks are
        # now split between VR and value fixers, the ORIGINAL raw gets passed in to
        # the value fixer hook. The raw needs to be re-updated to match the fixed
        # version before being passed to the next set of fixers... but there's already
        # been an event logged for any changes up to this point and we don't want to
        # duplicate an event.
        # Potential future improvement: change the event logging to better mesh with
        # updated pydicom behavior, so that there's no need to have a "silent" arg.
        raw = raw._replace(silent=True, VR=VR)

    if fixers := kwargs.get("raw_value_fixers"):
        for fx in fixers:
            raw = fx(raw, encoding=encoding, dataset=ds, **hooks.raw_element_kwargs)

    if read_ctx:
        read_ctx.update(raw)

    VR = t.cast(str, raw.VR)
    data["VR"] = VR
    data["value"] = convert_value(VR, raw, encoding)
