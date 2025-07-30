"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.standards._2129 import (
        ISO2812007BallBearingDynamicEquivalentLoadCalculator,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.standards._2129": [
            "ISO2812007BallBearingDynamicEquivalentLoadCalculator"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = ("ISO2812007BallBearingDynamicEquivalentLoadCalculator",)
