"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.creation_options._1265 import (
        CylindricalGearPairCreationOptions,
    )
    from mastapy._private.gears.gear_designs.creation_options._1266 import (
        DifferentialAssemblyCreationOptions,
    )
    from mastapy._private.gears.gear_designs.creation_options._1267 import (
        GearSetCreationOptions,
    )
    from mastapy._private.gears.gear_designs.creation_options._1268 import (
        HypoidGearSetCreationOptions,
    )
    from mastapy._private.gears.gear_designs.creation_options._1269 import (
        SpiralBevelGearSetCreationOptions,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.creation_options._1265": [
            "CylindricalGearPairCreationOptions"
        ],
        "_private.gears.gear_designs.creation_options._1266": [
            "DifferentialAssemblyCreationOptions"
        ],
        "_private.gears.gear_designs.creation_options._1267": [
            "GearSetCreationOptions"
        ],
        "_private.gears.gear_designs.creation_options._1268": [
            "HypoidGearSetCreationOptions"
        ],
        "_private.gears.gear_designs.creation_options._1269": [
            "SpiralBevelGearSetCreationOptions"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearPairCreationOptions",
    "DifferentialAssemblyCreationOptions",
    "GearSetCreationOptions",
    "HypoidGearSetCreationOptions",
    "SpiralBevelGearSetCreationOptions",
)
