"""Abstract file class and common helpers."""

import functools
import typing as t
from collections.abc import MutableMapping
from pathlib import Path

import yaml
from fw_meta import MetaData
from fw_utils import AnyFile, AnyPath, BinFile, open_any

__all__ = [
    "AnyFile",
    "AnyPath",
    "AttrMixin",
    "FieldsMixin",
    "File",
    "ReadOnly",
    "parse_yaml_value",
]


@functools.lru_cache(maxsize=4096)
def parse_yaml_value(value: str):
    """Return field value parsed with YAML syntax."""
    try:
        return yaml.safe_load(value)
    except Exception:
        return value


class AttrMixin:
    """Mixin for exposing dictionary keys as attributes.

    The magic methods `__getattr__`, `__setattr__` and `__delattr__` are simply
    wrapping calls to `__getitem__`, `__setitem__` and `__delitem__`.

    Subclasses need to use `object.__setattr__` to set actual attributes for the
    first time, ideally in the constructor. Once an attribute has been set using
    `object.__setattr__` it can be updated and accessed using the normal attr
    access.
    """

    getattr_proxy = None

    def __getattr__(self, name: str):
        """Get an attribute - syntax sugar using __getitem__.

        If getattr_proxy is set, attempt getattr through it first.
        """
        try:
            return object.__getattribute__(self, name)
        except AttributeError as exc:
            if f"object has no attribute {name!r}" not in exc.args[0]:
                raise  # pragma: no cover
        try:
            return object.__getattribute__(self.getattr_proxy, name)
        except AttributeError as exc:
            if f"object has no attribute {name!r}" not in exc.args[0]:
                raise  # pragma: no cover
        try:
            return self.__getitem__(name)
        except KeyError as exc:
            msg = f"{self.__class__.__name__!r} object has no attribute {name!r}"
            raise AttributeError(msg) from exc

    def __setattr__(self, name: str, value) -> None:
        """Set an attribute - syntax sugar using __setitem__."""
        try:
            object.__getattribute__(self, name)
        except AttributeError as exc:
            if f"object has no attribute {name!r}" not in exc.args[0]:
                raise  # pragma: no cover
            self.__setitem__(name, value)

    def __delattr__(self, name: str) -> None:
        """Delete an attribute - syntax sugar using __delitem__."""
        try:
            self.__delitem__(name)
        except KeyError as exc:
            msg = f"{self.__class__.__name__!r} object has no attribute {name!r}"
            raise AttributeError(msg) from exc


class FieldsMixin:
    """Mixin for data types where parsed data can be represented as dictionary."""

    fields: dict

    @staticmethod
    def canonize_key(key):
        """Default implementation of canonize key which returns the original key."""
        return key

    def __getitem__(self, key: str):
        """Get field value by name."""
        return self.fields[self.canonize_key(key)]

    def __setitem__(self, key: str, value) -> None:
        """Set field value by name."""
        self.fields[self.canonize_key(key)] = value

    def __delitem__(self, key: str) -> None:
        """Delete a field by name."""
        del self.fields[self.canonize_key(key)]

    def __iter__(self):
        """Return an iterator of the field names."""
        return iter(self.fields)

    def __len__(self) -> int:
        """Return the number of parsed fields."""
        return len(self.fields)

    def __dir__(self) -> t.List[str]:
        """Return list of attributes including field names."""
        return list(super().__dir__()) + list(self.fields.keys())


# TODO: remove type ignore when solved: https://github.com/python/mypy/issues/8539
@functools.total_ordering  # type: ignore
class File(AttrMixin, MutableMapping):  # noqa: PLW1641 (Obj does not implement hash)
    """Data-file base class defining the common interface for parsed files."""

    def __init__(self, file: AnyFile) -> None:
        """Read and parse a data-file - subclasses are expected to add parsing."""
        with open_any(file) as rfile:
            if not rfile.read(1):
                raise ValueError(f"Zero-byte file: {rfile}")
        # NOTE using object.__setattr__ to side-step AttrMixin
        object.__setattr__(self, "_file", rfile.localpath or rfile)
        object.__setattr__(self, "localpath", rfile.localpath)
        object.__setattr__(self, "filepath", rfile.metapath)

    @property
    def file(self) -> BinFile:
        """Return the underlying file opened for reading as a BinFile."""
        return open_any(self._file, mode="rb")

    @property
    def filename(self) -> t.Optional[str]:
        """Return the basename of the underlying file if it has a path."""
        return Path(self.filepath).name if self.filepath else None

    def get_meta(self) -> MetaData:
        """Return the default Flywheel metadata extracted from the file."""
        return MetaData({"file.name": self.filename})  # pragma: no cover

    @property
    def sort_key(self):
        """Return sort key used for comparing/ordering instances."""
        return self.filepath  # pragma: no cover

    def open_dst(self, file: t.Optional[AnyFile] = None) -> BinFile:
        """Open destination file for writing."""
        dst = file or self.localpath
        if not dst:
            raise ValueError("Save destination required")
        wfile = open_any(dst, mode="wb")
        if wfile.localpath:
            # update the file/path reference for subsequent save() calls
            object.__setattr__(self, "_file", wfile.localpath)
            object.__setattr__(self, "localpath", wfile.localpath)
        return wfile

    def save(self, file: AnyFile = None) -> None:
        """Save (potentially modified) data file."""
        raise NotImplementedError  # pragma: no cover

    def __eq__(self, other: object) -> bool:
        """Return that file equals other based on sort_key property."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Expected type {self.__class__}")
        return self.sort_key == other.sort_key

    def __lt__(self, other: object) -> bool:
        """Return that file is before other based on sort_key property."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Expected type {self.__class__}")
        return self.sort_key < other.sort_key

    def __repr__(self):
        """Return string representation of the data-file."""
        return f"{self.__class__.__name__}({self.filepath!r})"


class ReadOnly:
    """Mixin for read-only file types that don't support editing and saving."""

    def __setitem__(self, key: str, value) -> None:
        """Set field value by name."""
        raise TypeError(f"{self.__class__.__name__} is read-only")

    def __delitem__(self, key: str) -> None:
        """Delete a field by name."""
        raise TypeError(f"{self.__class__.__name__} is read-only")

    def save(self, file: AnyFile = None) -> None:
        """Save (potentially modified) data file."""
        raise TypeError(f"{self.__class__.__name__} is read-only")
