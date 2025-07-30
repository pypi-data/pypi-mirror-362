"""json file class."""

import codecs
import json
import typing as t

from dotty_dict import Dotty, dotty
from fw_meta import MetaData
from fw_utils import AnyFile, AnyPath

from .base import FieldsMixin, File


class JSON(FieldsMixin, File):
    """Json file format."""

    def __init__(self, file: AnyPath) -> None:
        """Read and parse a .json file.

        Args:
            file (AnyPath): File to load.
        """
        super().__init__(file)
        with self.file as rfile:
            reader = codecs.getreader("utf-8")
            fields = dotty(json.load(reader(rfile)))
        object.__setattr__(self, "fields", fields)
        object.__setattr__(self, "removed", set())

    def get_meta(self) -> MetaData:
        """Return the default Flywheel metadata of the JSON."""
        return MetaData({"file.type": "source code", "file.name": self.filename})

    def save(self, file: t.Optional[AnyFile] = None) -> None:
        """Saves the current contents to a json file."""
        fields_out = self.to_dict()
        with self.open_dst(file) as wfile:
            out = json.dumps(fields_out)
            wfile.write(out.encode())

    def __iter__(self):
        """Return iterator over object fields (top level keys only)."""
        return iter(dict(self.fields))

    def to_dict(self) -> dict:
        """Converts the current contents to a regular python dictionary."""
        return self.fields.to_dict()  # type: ignore

    def remove_blanks(self) -> None:
        """Remove blanks from the fields (recursively)."""
        sorted_keys = self.get_all_keys()
        for key in sorted_keys:
            # Keys are guaranteed to exist
            if self.fields[key] in [None, "", {}]:
                del self[key]
                self.removed.add(key)

    @staticmethod
    def _get_all_keys(d: t.Union[Dotty, dict]) -> list:
        """Get all keys in dotty format."""
        keys = []
        for k, v in d.items():
            keys += [k]
            if isinstance(v, (Dotty, dict)):
                subkeys = JSON._get_all_keys(v)
                keys += [f"{k}.{sk}" for sk in subkeys]
        return keys

    def get_all_keys(self) -> list:
        """Return all keys (even nested) from the object, sorted by depth."""
        keys = self._get_all_keys(self.fields)
        keys = sorted(keys, key=lambda x: x.count("."), reverse=True)
        return keys
