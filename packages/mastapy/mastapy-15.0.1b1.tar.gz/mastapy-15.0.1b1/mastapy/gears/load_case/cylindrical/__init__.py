"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.load_case.cylindrical._985 import (
        CylindricalGearLoadCase,
    )
    from mastapy._private.gears.load_case.cylindrical._986 import (
        CylindricalGearSetLoadCase,
    )
    from mastapy._private.gears.load_case.cylindrical._987 import (
        CylindricalMeshLoadCase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.load_case.cylindrical._985": ["CylindricalGearLoadCase"],
        "_private.gears.load_case.cylindrical._986": ["CylindricalGearSetLoadCase"],
        "_private.gears.load_case.cylindrical._987": ["CylindricalMeshLoadCase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearLoadCase",
    "CylindricalGearSetLoadCase",
    "CylindricalMeshLoadCase",
)
