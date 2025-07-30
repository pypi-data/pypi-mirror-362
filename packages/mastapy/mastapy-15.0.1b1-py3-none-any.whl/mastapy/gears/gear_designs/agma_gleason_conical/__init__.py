"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.agma_gleason_conical._1312 import (
        AGMAGleasonConicalAccuracyGrades,
    )
    from mastapy._private.gears.gear_designs.agma_gleason_conical._1313 import (
        AGMAGleasonConicalGearDesign,
    )
    from mastapy._private.gears.gear_designs.agma_gleason_conical._1314 import (
        AGMAGleasonConicalGearMeshDesign,
    )
    from mastapy._private.gears.gear_designs.agma_gleason_conical._1315 import (
        AGMAGleasonConicalGearSetDesign,
    )
    from mastapy._private.gears.gear_designs.agma_gleason_conical._1316 import (
        AGMAGleasonConicalMeshedGearDesign,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.agma_gleason_conical._1312": [
            "AGMAGleasonConicalAccuracyGrades"
        ],
        "_private.gears.gear_designs.agma_gleason_conical._1313": [
            "AGMAGleasonConicalGearDesign"
        ],
        "_private.gears.gear_designs.agma_gleason_conical._1314": [
            "AGMAGleasonConicalGearMeshDesign"
        ],
        "_private.gears.gear_designs.agma_gleason_conical._1315": [
            "AGMAGleasonConicalGearSetDesign"
        ],
        "_private.gears.gear_designs.agma_gleason_conical._1316": [
            "AGMAGleasonConicalMeshedGearDesign"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMAGleasonConicalAccuracyGrades",
    "AGMAGleasonConicalGearDesign",
    "AGMAGleasonConicalGearMeshDesign",
    "AGMAGleasonConicalGearSetDesign",
    "AGMAGleasonConicalMeshedGearDesign",
)
