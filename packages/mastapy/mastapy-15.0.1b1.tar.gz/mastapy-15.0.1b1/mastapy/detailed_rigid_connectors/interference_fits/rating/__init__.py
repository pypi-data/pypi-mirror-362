"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.detailed_rigid_connectors.interference_fits.rating._1634 import (
        InterferenceFitRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.detailed_rigid_connectors.interference_fits.rating._1634": [
            "InterferenceFitRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = ("InterferenceFitRating",)
