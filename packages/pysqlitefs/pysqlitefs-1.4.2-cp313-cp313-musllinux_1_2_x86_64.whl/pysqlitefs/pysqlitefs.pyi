"""

        Python bindings for sqlitefs
    
"""
from __future__ import annotations
import collections.abc
import typing
__all__ = ['Attributes', 'NodeAttribute', 'SQLiteFS', 'SQLiteFSNode', 'Stats']
class Attributes:
    """
    Members:
    
      FOLDER
    
      TOTAL_FLAGS
    """
    FOLDER: typing.ClassVar[Attributes]  # value = <Attributes.FOLDER: 0>
    TOTAL_FLAGS: typing.ClassVar[Attributes]  # value = <Attributes.TOTAL_FLAGS: 32>
    __members__: typing.ClassVar[dict[str, Attributes]]  # value = {'FOLDER': <Attributes.FOLDER: 0>, 'TOTAL_FLAGS': <Attributes.TOTAL_FLAGS: 32>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class NodeAttribute:
    def __getitem__(self, attribute: Attributes) -> bool:
        """
        Get node metainfo
        """
class SQLiteFS:
    def __init__(self, file_name: str, key: str = '') -> None:
        ...
    def cd(self, name: str) -> bool:
        """
        Change current working directory
        """
    def cp(self, src: str, target: str) -> bool:
        """
        Copy the file
        """
    def error(self) -> str:
        """
        Get the last error string
        """
    def getLoadFuncs(self) -> list[str]:
        """
        Get available load functions
        """
    def getSaveFuncs(self) -> list[str]:
        """
        Get available save functions
        """
    def ls(self, path: str = '.') -> list[SQLiteFSNode]:
        """
        List files in the directory
        """
    def mkdir(self, name: str) -> bool:
        """
        Create a new folder
        """
    def mv(self, src: str, target: str) -> bool:
        """
        Move the file
        """
    def path(self) -> str:
        """
        Get current path to the sqlitefs database file
        """
    def pwd(self) -> str:
        """
        Get current working directory
        """
    def read(self, name: str) -> bytes:
        """
        Read a file
        """
    def register_load_func(self, name: str, func: collections.abc.Callable[[bytes], bytes]) -> None:
        ...
    def register_save_func(self, name: str, func: collections.abc.Callable[[bytes], bytes]) -> None:
        ...
    def rm(self, name: str) -> bool:
        """
        Remove folder
        """
    def stats(self, path: str = '.') -> Stats:
        """
        Get information about directory
        """
    def vacuum(self) -> None:
        """
        Vacuum the database
        """
    def write(self, name: str, data: bytes, alg: str = 'raw') -> None:
        """
        Write a file
        """
class SQLiteFSNode:
    @property
    def attr(self) -> NodeAttribute:
        ...
    @property
    def compression(self) -> str:
        ...
    @property
    def id(self) -> int:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def parent_id(self) -> int:
        ...
    @property
    def size(self) -> int:
        ...
    @property
    def size_raw(self) -> int:
        ...
class Stats:
    @property
    def count(self) -> int:
        ...
    @property
    def size(self) -> int:
        ...
    @property
    def size_raw(self) -> int:
        ...
