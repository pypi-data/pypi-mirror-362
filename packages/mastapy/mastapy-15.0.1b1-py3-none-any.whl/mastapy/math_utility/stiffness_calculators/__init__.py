"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility.stiffness_calculators._1720 import (
        IndividualContactPosition,
    )
    from mastapy._private.math_utility.stiffness_calculators._1721 import (
        SurfaceToSurfaceContact,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility.stiffness_calculators._1720": [
            "IndividualContactPosition"
        ],
        "_private.math_utility.stiffness_calculators._1721": [
            "SurfaceToSurfaceContact"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "IndividualContactPosition",
    "SurfaceToSurfaceContact",
)
