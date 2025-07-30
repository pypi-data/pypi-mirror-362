"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.cylindrical.vdi._580 import (
        VDI2737InternalGearSingleFlankRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.cylindrical.vdi._580": [
            "VDI2737InternalGearSingleFlankRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = ("VDI2737InternalGearSingleFlankRating",)
