"""NIfTI-1 and NIfTI-2 (.nii.gz) file format."""

import nibabel
from fw_meta import MetaData

from .base import AnyPath, File


class Nifti(File):
    """NIfTI-1 and NIfTI-2 (.nii.gz) file format."""

    def __init__(self, file: AnyPath) -> None:
        """Read and parse a NIfTI-1 or NIfTI-2 file.

        Args:
            file (AnyPath): File to load.
        """
        super().__init__(file)
        try:
            object.__setattr__(self, "nifti", nibabel.load(self.localpath))
            object.__setattr__(self, "getattr_proxy", self.nifti)
        except nibabel.filebasedimages.ImageFileError as exc:
            raise ValueError(f"Invalid NIfTI file: {file}") from exc

    def get_meta(self) -> MetaData:
        """Return the default Flywheel metadata of the Nifti."""
        return MetaData({"file.type": "nifti", "file.name": self.filename})

    def save(self, file: AnyPath = None) -> None:  # type: ignore
        """Save nifti image."""
        nibabel.save(self.nifti, file or self.localpath)  # type: ignore

    def __getitem__(self, key: str):
        """Get header value by name."""
        return self.nifti.header[key]

    def __setitem__(self, key: str, value) -> None:
        """Set header value by name and value."""
        self.nifti.header[key] = value

    def __delitem__(self, key: str) -> None:
        """Delete header value."""
        raise TypeError("Nifti doesn't support field removal.")

    def __iter__(self):
        """Return iterator over nifti header."""
        return iter(self.nifti.header)

    def __len__(self) -> int:
        """Return length of nifti header."""
        return len(list(self.nifti.header.items()))
