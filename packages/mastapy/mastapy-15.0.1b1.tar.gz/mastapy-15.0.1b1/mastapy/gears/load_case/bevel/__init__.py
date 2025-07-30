"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.load_case.bevel._994 import BevelLoadCase
    from mastapy._private.gears.load_case.bevel._995 import BevelMeshLoadCase
    from mastapy._private.gears.load_case.bevel._996 import BevelSetLoadCase
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.load_case.bevel._994": ["BevelLoadCase"],
        "_private.gears.load_case.bevel._995": ["BevelMeshLoadCase"],
        "_private.gears.load_case.bevel._996": ["BevelSetLoadCase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BevelLoadCase",
    "BevelMeshLoadCase",
    "BevelSetLoadCase",
)
