"""JPG file format."""

import typing as t

from fw_meta import MetaData
from fw_utils import AnyFile
from PIL import Image

from .base import FieldsMixin, File
from .exif import EXIF


class JPG(FieldsMixin, File):
    """JPG data-file class."""

    def __init__(self, file: AnyFile) -> None:
        """Load and parse JPG files."""
        super().__init__(file)
        img = Image.open(self.file)
        object.__setattr__(self, "fields", EXIF.from_bytes(img.info.get("exif", b"")))
        object.__setattr__(self, "img", img)

    def get_meta(self) -> MetaData:
        """Return the default Flywheel metadata of the JPG."""
        return MetaData({"file.type": "image", "file.name": self.filename})

    def save(self, file: t.Optional[AnyFile] = None) -> None:
        """Save (potentially modified) data file."""
        with self.open_dst(file) as wfile:
            exif = t.cast(EXIF, self.fields).to_bytes()
            self.img.save(wfile, exif=exif, format="JPEG")
