"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_results.rolling.dysla._2323 import (
        DynamicBearingAnalysisOptions,
    )
    from mastapy._private.bearings.bearing_results.rolling.dysla._2324 import (
        RevolutionsType,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_results.rolling.dysla._2323": [
            "DynamicBearingAnalysisOptions"
        ],
        "_private.bearings.bearing_results.rolling.dysla._2324": ["RevolutionsType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DynamicBearingAnalysisOptions",
    "RevolutionsType",
)
