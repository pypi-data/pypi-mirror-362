"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.face._1093 import FaceGearDesign
    from mastapy._private.gears.gear_designs.face._1094 import (
        FaceGearDiameterFaceWidthSpecificationMethod,
    )
    from mastapy._private.gears.gear_designs.face._1095 import FaceGearMeshDesign
    from mastapy._private.gears.gear_designs.face._1096 import FaceGearMeshMicroGeometry
    from mastapy._private.gears.gear_designs.face._1097 import FaceGearMicroGeometry
    from mastapy._private.gears.gear_designs.face._1098 import FaceGearPinionDesign
    from mastapy._private.gears.gear_designs.face._1099 import FaceGearSetDesign
    from mastapy._private.gears.gear_designs.face._1100 import FaceGearSetMicroGeometry
    from mastapy._private.gears.gear_designs.face._1101 import FaceGearWheelDesign
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.face._1093": ["FaceGearDesign"],
        "_private.gears.gear_designs.face._1094": [
            "FaceGearDiameterFaceWidthSpecificationMethod"
        ],
        "_private.gears.gear_designs.face._1095": ["FaceGearMeshDesign"],
        "_private.gears.gear_designs.face._1096": ["FaceGearMeshMicroGeometry"],
        "_private.gears.gear_designs.face._1097": ["FaceGearMicroGeometry"],
        "_private.gears.gear_designs.face._1098": ["FaceGearPinionDesign"],
        "_private.gears.gear_designs.face._1099": ["FaceGearSetDesign"],
        "_private.gears.gear_designs.face._1100": ["FaceGearSetMicroGeometry"],
        "_private.gears.gear_designs.face._1101": ["FaceGearWheelDesign"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FaceGearDesign",
    "FaceGearDiameterFaceWidthSpecificationMethod",
    "FaceGearMeshDesign",
    "FaceGearMeshMicroGeometry",
    "FaceGearMicroGeometry",
    "FaceGearPinionDesign",
    "FaceGearSetDesign",
    "FaceGearSetMicroGeometry",
    "FaceGearWheelDesign",
)
