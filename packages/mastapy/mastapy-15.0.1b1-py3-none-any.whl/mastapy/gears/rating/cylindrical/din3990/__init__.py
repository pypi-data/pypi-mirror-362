"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.cylindrical.din3990._623 import (
        DIN3990GearSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical.din3990._624 import (
        DIN3990MeshSingleFlankRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.cylindrical.din3990._623": [
            "DIN3990GearSingleFlankRating"
        ],
        "_private.gears.rating.cylindrical.din3990._624": [
            "DIN3990MeshSingleFlankRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DIN3990GearSingleFlankRating",
    "DIN3990MeshSingleFlankRating",
)
