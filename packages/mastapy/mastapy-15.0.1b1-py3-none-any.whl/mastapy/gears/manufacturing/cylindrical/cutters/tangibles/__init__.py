"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._826 import (
        CutterShapeDefinition,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._827 import (
        CylindricalGearFormedWheelGrinderTangible,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._828 import (
        CylindricalGearHobShape,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._829 import (
        CylindricalGearShaperTangible,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._830 import (
        CylindricalGearShaverTangible,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._831 import (
        CylindricalGearWormGrinderShape,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._832 import (
        NamedPoint,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._833 import (
        RackShape,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._826": [
            "CutterShapeDefinition"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._827": [
            "CylindricalGearFormedWheelGrinderTangible"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._828": [
            "CylindricalGearHobShape"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._829": [
            "CylindricalGearShaperTangible"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._830": [
            "CylindricalGearShaverTangible"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._831": [
            "CylindricalGearWormGrinderShape"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._832": [
            "NamedPoint"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._833": [
            "RackShape"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CutterShapeDefinition",
    "CylindricalGearFormedWheelGrinderTangible",
    "CylindricalGearHobShape",
    "CylindricalGearShaperTangible",
    "CylindricalGearShaverTangible",
    "CylindricalGearWormGrinderShape",
    "NamedPoint",
    "RackShape",
)
