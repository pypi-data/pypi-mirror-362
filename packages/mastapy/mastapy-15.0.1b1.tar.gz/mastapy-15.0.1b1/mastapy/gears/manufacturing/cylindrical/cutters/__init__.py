"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.cylindrical.cutters._806 import (
        CurveInLinkedList,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._807 import (
        CustomisableEdgeProfile,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._808 import (
        CylindricalFormedWheelGrinderDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._809 import (
        CylindricalGearAbstractCutterDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._810 import (
        CylindricalGearFormGrindingWheel,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._811 import (
        CylindricalGearGrindingWorm,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._812 import (
        CylindricalGearHobDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._813 import (
        CylindricalGearPlungeShaver,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._814 import (
        CylindricalGearPlungeShaverDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._815 import (
        CylindricalGearRackDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._816 import (
        CylindricalGearRealCutterDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._817 import (
        CylindricalGearShaper,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._818 import (
        CylindricalGearShaver,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._819 import (
        CylindricalGearShaverDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._820 import (
        CylindricalWormGrinderDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._821 import (
        InvoluteCutterDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._822 import (
        MutableCommon,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._823 import (
        MutableCurve,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._824 import (
        MutableFillet,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._825 import (
        RoughCutterCreationSettings,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.cylindrical.cutters._806": ["CurveInLinkedList"],
        "_private.gears.manufacturing.cylindrical.cutters._807": [
            "CustomisableEdgeProfile"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._808": [
            "CylindricalFormedWheelGrinderDatabase"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._809": [
            "CylindricalGearAbstractCutterDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._810": [
            "CylindricalGearFormGrindingWheel"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._811": [
            "CylindricalGearGrindingWorm"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._812": [
            "CylindricalGearHobDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._813": [
            "CylindricalGearPlungeShaver"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._814": [
            "CylindricalGearPlungeShaverDatabase"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._815": [
            "CylindricalGearRackDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._816": [
            "CylindricalGearRealCutterDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._817": [
            "CylindricalGearShaper"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._818": [
            "CylindricalGearShaver"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._819": [
            "CylindricalGearShaverDatabase"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._820": [
            "CylindricalWormGrinderDatabase"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._821": [
            "InvoluteCutterDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._822": ["MutableCommon"],
        "_private.gears.manufacturing.cylindrical.cutters._823": ["MutableCurve"],
        "_private.gears.manufacturing.cylindrical.cutters._824": ["MutableFillet"],
        "_private.gears.manufacturing.cylindrical.cutters._825": [
            "RoughCutterCreationSettings"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CurveInLinkedList",
    "CustomisableEdgeProfile",
    "CylindricalFormedWheelGrinderDatabase",
    "CylindricalGearAbstractCutterDesign",
    "CylindricalGearFormGrindingWheel",
    "CylindricalGearGrindingWorm",
    "CylindricalGearHobDesign",
    "CylindricalGearPlungeShaver",
    "CylindricalGearPlungeShaverDatabase",
    "CylindricalGearRackDesign",
    "CylindricalGearRealCutterDesign",
    "CylindricalGearShaper",
    "CylindricalGearShaver",
    "CylindricalGearShaverDatabase",
    "CylindricalWormGrinderDatabase",
    "InvoluteCutterDesign",
    "MutableCommon",
    "MutableCurve",
    "MutableFillet",
    "RoughCutterCreationSettings",
)
