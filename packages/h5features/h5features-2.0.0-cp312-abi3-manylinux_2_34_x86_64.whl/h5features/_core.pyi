from collections.abc import Sequence
import enum
import os
from typing import Annotated, overload

from numpy.typing import ArrayLike


class Version(enum.Enum):
    """
    The different h5features format versions.

     This is **not** the version of the h5features library but the available
     versions of the underlying file format.
    """

    v1_0 = 0

    v1_1 = 1

    v1_2 = 2

    v2_0 = 3

class Item:
    def __init__(self, name: str, features: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C', writable=False)], times: Annotated[ArrayLike, dict(dtype='float64', order='C', writable=False)], properties: dict | None = None) -> Item:
        """Handle the features of a single item (e.g. a speech signal)."""

    def __eq__(self, other: Item) -> bool: ...

    def __ne__(self, other: Item) -> bool: ...

    @property
    def name(self) -> str:
        """The name of the item."""

    @property
    def dim(self) -> int:
        """The dimension of the features."""

    @property
    def size(self) -> int:
        """The number of vectors in the features."""

    @property
    def properties(self) -> dict:
        """The item's properties."""

    def features(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
        """The item's features."""

    def times(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
        """The item's timestamps."""

    def __repr__(self) -> str: ...

class Reader:
    def __init__(self, filename: str | os.PathLike, *, group: str = 'features') -> Reader:
        """Read :py:class:`.Item` instances from an HDF5 file."""

    def read(self, name: str, *, ignore_properties: bool = False) -> Item:
        """Read an :py:class:`.Item` from the HDF5 file."""

    def read_partial(self, name: str, start: float, stop: float, *, ignore_properties: bool = False) -> Item:
        """
        Partial read of an :py:class:`.Item` within the time interval ``[start, stop]``.
        """

    def read_all(self, *, ignore_properties: bool = False) -> list[Item]:
        """Read all the items stored in the file."""

    def items(self) -> list[str]:
        """The name of stored items."""

    @property
    def filename(self) -> str:
        """The name of the file being read."""

    @property
    def groupname(self) -> str:
        """The name of the group being read in the file."""

    @property
    def version(self) -> Version:
        """The :py:class:`.Version` of the h5features data in the group."""

    @staticmethod
    def list_groups(filename: str | os.PathLike) -> list[str]:
        """Return the list of groups in the specified HDF5 file."""

    def __repr__(self) -> str: ...

class Writer:
    def __init__(self, filename: str | os.PathLike, *, group: str = 'features', overwrite: bool = False, compress: bool = False, version: Version = Version.v2_0) -> Writer:
        """Write :py:class:`.Item` instances to an HDF5 file."""

    @overload
    def write(self, item: Item) -> None:
        """Write an :py:class:`.Item` to disk."""

    @overload
    def write(self, items: Sequence[Item]) -> None:
        """Write a sequence of :py:class:`.Item` to disk in parallel."""

    @property
    def version(self) -> Version:
        """The h5features format :py:class:`.Version` being written."""

    @property
    def filename(self) -> str:
        """The HDF5 file name."""

    @property
    def groupname(self) -> str:
        """The HDF5 group name."""

    def __repr__(self) -> str: ...
