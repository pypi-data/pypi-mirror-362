"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.conical.micro_geometry._1292 import (
        ConicalGearBiasModification,
    )
    from mastapy._private.gears.gear_designs.conical.micro_geometry._1293 import (
        ConicalGearFlankMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.conical.micro_geometry._1294 import (
        ConicalGearLeadModification,
    )
    from mastapy._private.gears.gear_designs.conical.micro_geometry._1295 import (
        ConicalGearProfileModification,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.conical.micro_geometry._1292": [
            "ConicalGearBiasModification"
        ],
        "_private.gears.gear_designs.conical.micro_geometry._1293": [
            "ConicalGearFlankMicroGeometry"
        ],
        "_private.gears.gear_designs.conical.micro_geometry._1294": [
            "ConicalGearLeadModification"
        ],
        "_private.gears.gear_designs.conical.micro_geometry._1295": [
            "ConicalGearProfileModification"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearBiasModification",
    "ConicalGearFlankMicroGeometry",
    "ConicalGearLeadModification",
    "ConicalGearProfileModification",
)
