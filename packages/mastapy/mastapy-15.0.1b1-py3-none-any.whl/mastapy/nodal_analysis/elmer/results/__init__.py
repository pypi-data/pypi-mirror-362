"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.elmer.results._259 import Data
    from mastapy._private.nodal_analysis.elmer.results._260 import Data1D
    from mastapy._private.nodal_analysis.elmer.results._261 import Data3D
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.elmer.results._259": ["Data"],
        "_private.nodal_analysis.elmer.results._260": ["Data1D"],
        "_private.nodal_analysis.elmer.results._261": ["Data3D"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Data",
    "Data1D",
    "Data3D",
)
