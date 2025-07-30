"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.straight_bevel._1065 import (
        StraightBevelGearDesign,
    )
    from mastapy._private.gears.gear_designs.straight_bevel._1066 import (
        StraightBevelGearMeshDesign,
    )
    from mastapy._private.gears.gear_designs.straight_bevel._1067 import (
        StraightBevelGearSetDesign,
    )
    from mastapy._private.gears.gear_designs.straight_bevel._1068 import (
        StraightBevelMeshedGearDesign,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.straight_bevel._1065": ["StraightBevelGearDesign"],
        "_private.gears.gear_designs.straight_bevel._1066": [
            "StraightBevelGearMeshDesign"
        ],
        "_private.gears.gear_designs.straight_bevel._1067": [
            "StraightBevelGearSetDesign"
        ],
        "_private.gears.gear_designs.straight_bevel._1068": [
            "StraightBevelMeshedGearDesign"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "StraightBevelGearDesign",
    "StraightBevelGearMeshDesign",
    "StraightBevelGearSetDesign",
    "StraightBevelMeshedGearDesign",
)
