"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.load_case.worm._979 import WormGearLoadCase
    from mastapy._private.gears.load_case.worm._980 import WormGearSetLoadCase
    from mastapy._private.gears.load_case.worm._981 import WormMeshLoadCase
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.load_case.worm._979": ["WormGearLoadCase"],
        "_private.gears.load_case.worm._980": ["WormGearSetLoadCase"],
        "_private.gears.load_case.worm._981": ["WormMeshLoadCase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "WormGearLoadCase",
    "WormGearSetLoadCase",
    "WormMeshLoadCase",
)
