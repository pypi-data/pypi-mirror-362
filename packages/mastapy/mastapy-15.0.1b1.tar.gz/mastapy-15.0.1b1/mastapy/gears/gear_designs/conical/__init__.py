"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.conical._1270 import ActiveConicalFlank
    from mastapy._private.gears.gear_designs.conical._1271 import (
        BacklashDistributionRule,
    )
    from mastapy._private.gears.gear_designs.conical._1272 import ConicalFlanks
    from mastapy._private.gears.gear_designs.conical._1273 import ConicalGearCutter
    from mastapy._private.gears.gear_designs.conical._1274 import ConicalGearDesign
    from mastapy._private.gears.gear_designs.conical._1275 import ConicalGearMeshDesign
    from mastapy._private.gears.gear_designs.conical._1276 import ConicalGearSetDesign
    from mastapy._private.gears.gear_designs.conical._1277 import (
        ConicalMachineSettingCalculationMethods,
    )
    from mastapy._private.gears.gear_designs.conical._1278 import (
        ConicalManufactureMethods,
    )
    from mastapy._private.gears.gear_designs.conical._1279 import (
        ConicalMeshedGearDesign,
    )
    from mastapy._private.gears.gear_designs.conical._1280 import (
        ConicalMeshMisalignments,
    )
    from mastapy._private.gears.gear_designs.conical._1281 import CutterBladeType
    from mastapy._private.gears.gear_designs.conical._1282 import CutterGaugeLengths
    from mastapy._private.gears.gear_designs.conical._1283 import DummyConicalGearCutter
    from mastapy._private.gears.gear_designs.conical._1284 import FrontEndTypes
    from mastapy._private.gears.gear_designs.conical._1285 import (
        GleasonSafetyRequirements,
    )
    from mastapy._private.gears.gear_designs.conical._1286 import (
        KIMoSBevelHypoidSingleLoadCaseResultsData,
    )
    from mastapy._private.gears.gear_designs.conical._1287 import (
        KIMoSBevelHypoidSingleRotationAngleResult,
    )
    from mastapy._private.gears.gear_designs.conical._1288 import (
        KlingelnbergFinishingMethods,
    )
    from mastapy._private.gears.gear_designs.conical._1289 import (
        LoadDistributionFactorMethods,
    )
    from mastapy._private.gears.gear_designs.conical._1290 import TopremEntryType
    from mastapy._private.gears.gear_designs.conical._1291 import TopremLetter
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.conical._1270": ["ActiveConicalFlank"],
        "_private.gears.gear_designs.conical._1271": ["BacklashDistributionRule"],
        "_private.gears.gear_designs.conical._1272": ["ConicalFlanks"],
        "_private.gears.gear_designs.conical._1273": ["ConicalGearCutter"],
        "_private.gears.gear_designs.conical._1274": ["ConicalGearDesign"],
        "_private.gears.gear_designs.conical._1275": ["ConicalGearMeshDesign"],
        "_private.gears.gear_designs.conical._1276": ["ConicalGearSetDesign"],
        "_private.gears.gear_designs.conical._1277": [
            "ConicalMachineSettingCalculationMethods"
        ],
        "_private.gears.gear_designs.conical._1278": ["ConicalManufactureMethods"],
        "_private.gears.gear_designs.conical._1279": ["ConicalMeshedGearDesign"],
        "_private.gears.gear_designs.conical._1280": ["ConicalMeshMisalignments"],
        "_private.gears.gear_designs.conical._1281": ["CutterBladeType"],
        "_private.gears.gear_designs.conical._1282": ["CutterGaugeLengths"],
        "_private.gears.gear_designs.conical._1283": ["DummyConicalGearCutter"],
        "_private.gears.gear_designs.conical._1284": ["FrontEndTypes"],
        "_private.gears.gear_designs.conical._1285": ["GleasonSafetyRequirements"],
        "_private.gears.gear_designs.conical._1286": [
            "KIMoSBevelHypoidSingleLoadCaseResultsData"
        ],
        "_private.gears.gear_designs.conical._1287": [
            "KIMoSBevelHypoidSingleRotationAngleResult"
        ],
        "_private.gears.gear_designs.conical._1288": ["KlingelnbergFinishingMethods"],
        "_private.gears.gear_designs.conical._1289": ["LoadDistributionFactorMethods"],
        "_private.gears.gear_designs.conical._1290": ["TopremEntryType"],
        "_private.gears.gear_designs.conical._1291": ["TopremLetter"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ActiveConicalFlank",
    "BacklashDistributionRule",
    "ConicalFlanks",
    "ConicalGearCutter",
    "ConicalGearDesign",
    "ConicalGearMeshDesign",
    "ConicalGearSetDesign",
    "ConicalMachineSettingCalculationMethods",
    "ConicalManufactureMethods",
    "ConicalMeshedGearDesign",
    "ConicalMeshMisalignments",
    "CutterBladeType",
    "CutterGaugeLengths",
    "DummyConicalGearCutter",
    "FrontEndTypes",
    "GleasonSafetyRequirements",
    "KIMoSBevelHypoidSingleLoadCaseResultsData",
    "KIMoSBevelHypoidSingleRotationAngleResult",
    "KlingelnbergFinishingMethods",
    "LoadDistributionFactorMethods",
    "TopremEntryType",
    "TopremLetter",
)
