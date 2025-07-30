"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel._1077 import (
        KlingelnbergCycloPalloidSpiralBevelGearDesign,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel._1078 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshDesign,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel._1079 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetDesign,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel._1080 import (
        KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.klingelnberg_spiral_bevel._1077": [
            "KlingelnbergCycloPalloidSpiralBevelGearDesign"
        ],
        "_private.gears.gear_designs.klingelnberg_spiral_bevel._1078": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshDesign"
        ],
        "_private.gears.gear_designs.klingelnberg_spiral_bevel._1079": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetDesign"
        ],
        "_private.gears.gear_designs.klingelnberg_spiral_bevel._1080": [
            "KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "KlingelnbergCycloPalloidSpiralBevelGearDesign",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshDesign",
    "KlingelnbergCycloPalloidSpiralBevelGearSetDesign",
    "KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign",
)
