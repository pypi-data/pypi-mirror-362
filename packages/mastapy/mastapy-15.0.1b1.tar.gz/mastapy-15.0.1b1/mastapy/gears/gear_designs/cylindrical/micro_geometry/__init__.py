"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1206 import (
        CylindricalGearBiasModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1207 import (
        CylindricalGearCommonFlankMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1208 import (
        CylindricalGearFlankMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1209 import (
        CylindricalGearLeadModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1210 import (
        CylindricalGearLeadModificationAtProfilePosition,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1211 import (
        CylindricalGearMeshMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1212 import (
        CylindricalGearMeshMicroGeometryDutyCycle,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1213 import (
        CylindricalGearMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1214 import (
        CylindricalGearMicroGeometryBase,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1215 import (
        CylindricalGearMicroGeometryDutyCycle,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1216 import (
        CylindricalGearMicroGeometryMap,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1217 import (
        CylindricalGearMicroGeometryPerTooth,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1218 import (
        CylindricalGearProfileModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1219 import (
        CylindricalGearProfileModificationAtFaceWidthPosition,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1220 import (
        CylindricalGearSetMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1221 import (
        CylindricalGearSetMicroGeometryDutyCycle,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1222 import (
        CylindricalGearToothMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1223 import (
        CylindricalGearTriangularEndModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1224 import (
        CylindricalGearTriangularEndModificationAtOrientation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1225 import (
        DrawDefiningGearOrBoth,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1226 import (
        GearAlignment,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1227 import (
        LeadFormReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1228 import (
        LeadModificationForCustomer102CAD,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1229 import (
        LeadReliefSpecificationForCustomer102,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1230 import (
        LeadReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1231 import (
        LeadSlopeReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1232 import (
        LinearCylindricalGearTriangularEndModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1233 import (
        MeasuredMapDataTypes,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1234 import (
        MeshAlignment,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1235 import (
        MeshedCylindricalGearFlankMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1236 import (
        MeshedCylindricalGearMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1237 import (
        MicroGeometryLeadToleranceChartView,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1238 import (
        MicroGeometryViewingOptions,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1239 import (
        ModificationForCustomer102CAD,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1240 import (
        ParabolicCylindricalGearTriangularEndModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1241 import (
        ProfileFormReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1242 import (
        ProfileModificationForCustomer102CAD,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1243 import (
        ProfileReliefSpecificationForCustomer102,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1244 import (
        ProfileReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1245 import (
        ProfileSlopeReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1246 import (
        ReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1247 import (
        SingleCylindricalGearTriangularEndModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1248 import (
        TotalLeadReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1249 import (
        TotalProfileReliefWithDeviation,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.cylindrical.micro_geometry._1206": [
            "CylindricalGearBiasModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1207": [
            "CylindricalGearCommonFlankMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1208": [
            "CylindricalGearFlankMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1209": [
            "CylindricalGearLeadModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1210": [
            "CylindricalGearLeadModificationAtProfilePosition"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1211": [
            "CylindricalGearMeshMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1212": [
            "CylindricalGearMeshMicroGeometryDutyCycle"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1213": [
            "CylindricalGearMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1214": [
            "CylindricalGearMicroGeometryBase"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1215": [
            "CylindricalGearMicroGeometryDutyCycle"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1216": [
            "CylindricalGearMicroGeometryMap"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1217": [
            "CylindricalGearMicroGeometryPerTooth"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1218": [
            "CylindricalGearProfileModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1219": [
            "CylindricalGearProfileModificationAtFaceWidthPosition"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1220": [
            "CylindricalGearSetMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1221": [
            "CylindricalGearSetMicroGeometryDutyCycle"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1222": [
            "CylindricalGearToothMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1223": [
            "CylindricalGearTriangularEndModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1224": [
            "CylindricalGearTriangularEndModificationAtOrientation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1225": [
            "DrawDefiningGearOrBoth"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1226": [
            "GearAlignment"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1227": [
            "LeadFormReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1228": [
            "LeadModificationForCustomer102CAD"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1229": [
            "LeadReliefSpecificationForCustomer102"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1230": [
            "LeadReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1231": [
            "LeadSlopeReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1232": [
            "LinearCylindricalGearTriangularEndModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1233": [
            "MeasuredMapDataTypes"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1234": [
            "MeshAlignment"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1235": [
            "MeshedCylindricalGearFlankMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1236": [
            "MeshedCylindricalGearMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1237": [
            "MicroGeometryLeadToleranceChartView"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1238": [
            "MicroGeometryViewingOptions"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1239": [
            "ModificationForCustomer102CAD"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1240": [
            "ParabolicCylindricalGearTriangularEndModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1241": [
            "ProfileFormReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1242": [
            "ProfileModificationForCustomer102CAD"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1243": [
            "ProfileReliefSpecificationForCustomer102"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1244": [
            "ProfileReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1245": [
            "ProfileSlopeReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1246": [
            "ReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1247": [
            "SingleCylindricalGearTriangularEndModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1248": [
            "TotalLeadReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1249": [
            "TotalProfileReliefWithDeviation"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearBiasModification",
    "CylindricalGearCommonFlankMicroGeometry",
    "CylindricalGearFlankMicroGeometry",
    "CylindricalGearLeadModification",
    "CylindricalGearLeadModificationAtProfilePosition",
    "CylindricalGearMeshMicroGeometry",
    "CylindricalGearMeshMicroGeometryDutyCycle",
    "CylindricalGearMicroGeometry",
    "CylindricalGearMicroGeometryBase",
    "CylindricalGearMicroGeometryDutyCycle",
    "CylindricalGearMicroGeometryMap",
    "CylindricalGearMicroGeometryPerTooth",
    "CylindricalGearProfileModification",
    "CylindricalGearProfileModificationAtFaceWidthPosition",
    "CylindricalGearSetMicroGeometry",
    "CylindricalGearSetMicroGeometryDutyCycle",
    "CylindricalGearToothMicroGeometry",
    "CylindricalGearTriangularEndModification",
    "CylindricalGearTriangularEndModificationAtOrientation",
    "DrawDefiningGearOrBoth",
    "GearAlignment",
    "LeadFormReliefWithDeviation",
    "LeadModificationForCustomer102CAD",
    "LeadReliefSpecificationForCustomer102",
    "LeadReliefWithDeviation",
    "LeadSlopeReliefWithDeviation",
    "LinearCylindricalGearTriangularEndModification",
    "MeasuredMapDataTypes",
    "MeshAlignment",
    "MeshedCylindricalGearFlankMicroGeometry",
    "MeshedCylindricalGearMicroGeometry",
    "MicroGeometryLeadToleranceChartView",
    "MicroGeometryViewingOptions",
    "ModificationForCustomer102CAD",
    "ParabolicCylindricalGearTriangularEndModification",
    "ProfileFormReliefWithDeviation",
    "ProfileModificationForCustomer102CAD",
    "ProfileReliefSpecificationForCustomer102",
    "ProfileReliefWithDeviation",
    "ProfileSlopeReliefWithDeviation",
    "ReliefWithDeviation",
    "SingleCylindricalGearTriangularEndModification",
    "TotalLeadReliefWithDeviation",
    "TotalProfileReliefWithDeviation",
)
