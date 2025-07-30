"""Module for defining types used in mastapy."""

import os

try:
    from typing import TypeAlias

    PathLike: TypeAlias = str | os.PathLike[str]
except ImportError:
    PathLike = str | os.PathLike[str]
