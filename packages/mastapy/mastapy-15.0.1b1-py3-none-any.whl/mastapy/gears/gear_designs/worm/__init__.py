"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.worm._1060 import WormDesign
    from mastapy._private.gears.gear_designs.worm._1061 import WormGearDesign
    from mastapy._private.gears.gear_designs.worm._1062 import WormGearMeshDesign
    from mastapy._private.gears.gear_designs.worm._1063 import WormGearSetDesign
    from mastapy._private.gears.gear_designs.worm._1064 import WormWheelDesign
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.worm._1060": ["WormDesign"],
        "_private.gears.gear_designs.worm._1061": ["WormGearDesign"],
        "_private.gears.gear_designs.worm._1062": ["WormGearMeshDesign"],
        "_private.gears.gear_designs.worm._1063": ["WormGearSetDesign"],
        "_private.gears.gear_designs.worm._1064": ["WormWheelDesign"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "WormDesign",
    "WormGearDesign",
    "WormGearMeshDesign",
    "WormGearSetDesign",
    "WormWheelDesign",
)
