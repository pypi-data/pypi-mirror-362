"""Define PathOrStr as a type alias or at least as a union"""

from sys import version_info
from typing import Union
from pathlib import Path

__all__ = ['PathOrStr']

PathOrStr = Union[Path, str]
if version_info >= (3, 10):
    PathOrStr = Path | str
if version_info >= (3, 12):
    type PathOrStr = PathOrStr
