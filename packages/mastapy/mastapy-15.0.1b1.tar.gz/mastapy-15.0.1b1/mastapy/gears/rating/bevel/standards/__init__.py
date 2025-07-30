"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.bevel.standards._648 import (
        AGMASpiralBevelGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._649 import (
        AGMASpiralBevelMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._650 import (
        GleasonSpiralBevelGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._651 import (
        GleasonSpiralBevelMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._652 import (
        SpiralBevelGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._653 import (
        SpiralBevelMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._654 import (
        SpiralBevelRateableGear,
    )
    from mastapy._private.gears.rating.bevel.standards._655 import (
        SpiralBevelRateableMesh,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.bevel.standards._648": [
            "AGMASpiralBevelGearSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._649": [
            "AGMASpiralBevelMeshSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._650": [
            "GleasonSpiralBevelGearSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._651": [
            "GleasonSpiralBevelMeshSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._652": [
            "SpiralBevelGearSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._653": [
            "SpiralBevelMeshSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._654": ["SpiralBevelRateableGear"],
        "_private.gears.rating.bevel.standards._655": ["SpiralBevelRateableMesh"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMASpiralBevelGearSingleFlankRating",
    "AGMASpiralBevelMeshSingleFlankRating",
    "GleasonSpiralBevelGearSingleFlankRating",
    "GleasonSpiralBevelMeshSingleFlankRating",
    "SpiralBevelGearSingleFlankRating",
    "SpiralBevelMeshSingleFlankRating",
    "SpiralBevelRateableGear",
    "SpiralBevelRateableMesh",
)
