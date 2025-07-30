"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines._1365 import AbstractStator
    from mastapy._private.electric_machines._1366 import AbstractToothAndSlot
    from mastapy._private.electric_machines._1367 import CADConductor
    from mastapy._private.electric_machines._1368 import CADElectricMachineDetail
    from mastapy._private.electric_machines._1369 import CADFieldWindingSpecification
    from mastapy._private.electric_machines._1370 import CADMagnetDetails
    from mastapy._private.electric_machines._1371 import CADMagnetsForLayer
    from mastapy._private.electric_machines._1372 import CADRotor
    from mastapy._private.electric_machines._1373 import CADStator
    from mastapy._private.electric_machines._1374 import CADToothAndSlot
    from mastapy._private.electric_machines._1375 import CADWoundFieldSynchronousRotor
    from mastapy._private.electric_machines._1376 import Coil
    from mastapy._private.electric_machines._1377 import CoilPositionInSlot
    from mastapy._private.electric_machines._1378 import CoolingChannelShape
    from mastapy._private.electric_machines._1379 import CoolingDuctLayerSpecification
    from mastapy._private.electric_machines._1380 import CoolingDuctShape
    from mastapy._private.electric_machines._1381 import (
        CoreLossBuildFactorSpecificationMethod,
    )
    from mastapy._private.electric_machines._1382 import CoreLossCoefficients
    from mastapy._private.electric_machines._1383 import DoubleLayerWindingSlotPositions
    from mastapy._private.electric_machines._1384 import DQAxisConvention
    from mastapy._private.electric_machines._1385 import Eccentricity
    from mastapy._private.electric_machines._1386 import ElectricMachineDesignBase
    from mastapy._private.electric_machines._1387 import ElectricMachineDetail
    from mastapy._private.electric_machines._1388 import (
        ElectricMachineDetailInitialInformation,
    )
    from mastapy._private.electric_machines._1389 import (
        ElectricMachineElectromagneticAndThermalMeshingOptions,
    )
    from mastapy._private.electric_machines._1390 import ElectricMachineGroup
    from mastapy._private.electric_machines._1391 import (
        ElectricMachineMechanicalAnalysisMeshingOptions,
    )
    from mastapy._private.electric_machines._1392 import ElectricMachineMeshingOptions
    from mastapy._private.electric_machines._1393 import (
        ElectricMachineMeshingOptionsBase,
    )
    from mastapy._private.electric_machines._1394 import ElectricMachineSetup
    from mastapy._private.electric_machines._1395 import ElectricMachineSetupBase
    from mastapy._private.electric_machines._1396 import (
        ElectricMachineThermalMeshingOptions,
    )
    from mastapy._private.electric_machines._1397 import ElectricMachineType
    from mastapy._private.electric_machines._1398 import FieldWindingSpecification
    from mastapy._private.electric_machines._1399 import FieldWindingSpecificationBase
    from mastapy._private.electric_machines._1400 import FillFactorSpecificationMethod
    from mastapy._private.electric_machines._1401 import FluxBarriers
    from mastapy._private.electric_machines._1402 import FluxBarrierOrWeb
    from mastapy._private.electric_machines._1403 import FluxBarrierStyle
    from mastapy._private.electric_machines._1404 import GeneralElectricMachineMaterial
    from mastapy._private.electric_machines._1405 import (
        GeneralElectricMachineMaterialDatabase,
    )
    from mastapy._private.electric_machines._1406 import HairpinConductor
    from mastapy._private.electric_machines._1407 import (
        HarmonicLoadDataControlExcitationOptionForElectricMachineMode,
    )
    from mastapy._private.electric_machines._1408 import (
        IndividualConductorSpecificationSource,
    )
    from mastapy._private.electric_machines._1409 import (
        InteriorPermanentMagnetAndSynchronousReluctanceRotor,
    )
    from mastapy._private.electric_machines._1410 import InteriorPermanentMagnetMachine
    from mastapy._private.electric_machines._1411 import (
        IronLossCoefficientSpecificationMethod,
    )
    from mastapy._private.electric_machines._1412 import MagnetClearance
    from mastapy._private.electric_machines._1413 import MagnetConfiguration
    from mastapy._private.electric_machines._1414 import MagnetData
    from mastapy._private.electric_machines._1415 import MagnetDesign
    from mastapy._private.electric_machines._1416 import MagnetForLayer
    from mastapy._private.electric_machines._1417 import MagnetisationDirection
    from mastapy._private.electric_machines._1418 import MagnetMaterial
    from mastapy._private.electric_machines._1419 import MagnetMaterialDatabase
    from mastapy._private.electric_machines._1420 import MotorRotorSideFaceDetail
    from mastapy._private.electric_machines._1421 import NonCADElectricMachineDetail
    from mastapy._private.electric_machines._1422 import NotchShape
    from mastapy._private.electric_machines._1423 import NotchSpecification
    from mastapy._private.electric_machines._1424 import (
        PermanentMagnetAssistedSynchronousReluctanceMachine,
    )
    from mastapy._private.electric_machines._1425 import PermanentMagnetRotor
    from mastapy._private.electric_machines._1426 import Phase
    from mastapy._private.electric_machines._1427 import RegionID
    from mastapy._private.electric_machines._1428 import ResultsLocationsSpecification
    from mastapy._private.electric_machines._1429 import Rotor
    from mastapy._private.electric_machines._1430 import RotorInternalLayerSpecification
    from mastapy._private.electric_machines._1431 import RotorSkewSlice
    from mastapy._private.electric_machines._1432 import RotorType
    from mastapy._private.electric_machines._1433 import SingleOrDoubleLayerWindings
    from mastapy._private.electric_machines._1434 import SlotSectionDetail
    from mastapy._private.electric_machines._1435 import Stator
    from mastapy._private.electric_machines._1436 import StatorCutoutSpecification
    from mastapy._private.electric_machines._1437 import StatorRotorMaterial
    from mastapy._private.electric_machines._1438 import StatorRotorMaterialDatabase
    from mastapy._private.electric_machines._1439 import SurfacePermanentMagnetMachine
    from mastapy._private.electric_machines._1440 import SurfacePermanentMagnetRotor
    from mastapy._private.electric_machines._1441 import SynchronousReluctanceMachine
    from mastapy._private.electric_machines._1442 import ToothAndSlot
    from mastapy._private.electric_machines._1443 import ToothSlotStyle
    from mastapy._private.electric_machines._1444 import ToothTaperSpecification
    from mastapy._private.electric_machines._1445 import (
        TwoDimensionalFEModelForAnalysis,
    )
    from mastapy._private.electric_machines._1446 import (
        TwoDimensionalFEModelForElectromagneticAnalysis,
    )
    from mastapy._private.electric_machines._1447 import (
        TwoDimensionalFEModelForMechanicalAnalysis,
    )
    from mastapy._private.electric_machines._1448 import UShapedLayerSpecification
    from mastapy._private.electric_machines._1449 import VShapedMagnetLayerSpecification
    from mastapy._private.electric_machines._1450 import WindingConductor
    from mastapy._private.electric_machines._1451 import WindingConnection
    from mastapy._private.electric_machines._1452 import WindingMaterial
    from mastapy._private.electric_machines._1453 import WindingMaterialDatabase
    from mastapy._private.electric_machines._1454 import Windings
    from mastapy._private.electric_machines._1455 import WindingsViewer
    from mastapy._private.electric_machines._1456 import WindingType
    from mastapy._private.electric_machines._1457 import WireSizeSpecificationMethod
    from mastapy._private.electric_machines._1458 import WoundFieldSynchronousMachine
    from mastapy._private.electric_machines._1459 import WoundFieldSynchronousRotor
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines._1365": ["AbstractStator"],
        "_private.electric_machines._1366": ["AbstractToothAndSlot"],
        "_private.electric_machines._1367": ["CADConductor"],
        "_private.electric_machines._1368": ["CADElectricMachineDetail"],
        "_private.electric_machines._1369": ["CADFieldWindingSpecification"],
        "_private.electric_machines._1370": ["CADMagnetDetails"],
        "_private.electric_machines._1371": ["CADMagnetsForLayer"],
        "_private.electric_machines._1372": ["CADRotor"],
        "_private.electric_machines._1373": ["CADStator"],
        "_private.electric_machines._1374": ["CADToothAndSlot"],
        "_private.electric_machines._1375": ["CADWoundFieldSynchronousRotor"],
        "_private.electric_machines._1376": ["Coil"],
        "_private.electric_machines._1377": ["CoilPositionInSlot"],
        "_private.electric_machines._1378": ["CoolingChannelShape"],
        "_private.electric_machines._1379": ["CoolingDuctLayerSpecification"],
        "_private.electric_machines._1380": ["CoolingDuctShape"],
        "_private.electric_machines._1381": ["CoreLossBuildFactorSpecificationMethod"],
        "_private.electric_machines._1382": ["CoreLossCoefficients"],
        "_private.electric_machines._1383": ["DoubleLayerWindingSlotPositions"],
        "_private.electric_machines._1384": ["DQAxisConvention"],
        "_private.electric_machines._1385": ["Eccentricity"],
        "_private.electric_machines._1386": ["ElectricMachineDesignBase"],
        "_private.electric_machines._1387": ["ElectricMachineDetail"],
        "_private.electric_machines._1388": ["ElectricMachineDetailInitialInformation"],
        "_private.electric_machines._1389": [
            "ElectricMachineElectromagneticAndThermalMeshingOptions"
        ],
        "_private.electric_machines._1390": ["ElectricMachineGroup"],
        "_private.electric_machines._1391": [
            "ElectricMachineMechanicalAnalysisMeshingOptions"
        ],
        "_private.electric_machines._1392": ["ElectricMachineMeshingOptions"],
        "_private.electric_machines._1393": ["ElectricMachineMeshingOptionsBase"],
        "_private.electric_machines._1394": ["ElectricMachineSetup"],
        "_private.electric_machines._1395": ["ElectricMachineSetupBase"],
        "_private.electric_machines._1396": ["ElectricMachineThermalMeshingOptions"],
        "_private.electric_machines._1397": ["ElectricMachineType"],
        "_private.electric_machines._1398": ["FieldWindingSpecification"],
        "_private.electric_machines._1399": ["FieldWindingSpecificationBase"],
        "_private.electric_machines._1400": ["FillFactorSpecificationMethod"],
        "_private.electric_machines._1401": ["FluxBarriers"],
        "_private.electric_machines._1402": ["FluxBarrierOrWeb"],
        "_private.electric_machines._1403": ["FluxBarrierStyle"],
        "_private.electric_machines._1404": ["GeneralElectricMachineMaterial"],
        "_private.electric_machines._1405": ["GeneralElectricMachineMaterialDatabase"],
        "_private.electric_machines._1406": ["HairpinConductor"],
        "_private.electric_machines._1407": [
            "HarmonicLoadDataControlExcitationOptionForElectricMachineMode"
        ],
        "_private.electric_machines._1408": ["IndividualConductorSpecificationSource"],
        "_private.electric_machines._1409": [
            "InteriorPermanentMagnetAndSynchronousReluctanceRotor"
        ],
        "_private.electric_machines._1410": ["InteriorPermanentMagnetMachine"],
        "_private.electric_machines._1411": ["IronLossCoefficientSpecificationMethod"],
        "_private.electric_machines._1412": ["MagnetClearance"],
        "_private.electric_machines._1413": ["MagnetConfiguration"],
        "_private.electric_machines._1414": ["MagnetData"],
        "_private.electric_machines._1415": ["MagnetDesign"],
        "_private.electric_machines._1416": ["MagnetForLayer"],
        "_private.electric_machines._1417": ["MagnetisationDirection"],
        "_private.electric_machines._1418": ["MagnetMaterial"],
        "_private.electric_machines._1419": ["MagnetMaterialDatabase"],
        "_private.electric_machines._1420": ["MotorRotorSideFaceDetail"],
        "_private.electric_machines._1421": ["NonCADElectricMachineDetail"],
        "_private.electric_machines._1422": ["NotchShape"],
        "_private.electric_machines._1423": ["NotchSpecification"],
        "_private.electric_machines._1424": [
            "PermanentMagnetAssistedSynchronousReluctanceMachine"
        ],
        "_private.electric_machines._1425": ["PermanentMagnetRotor"],
        "_private.electric_machines._1426": ["Phase"],
        "_private.electric_machines._1427": ["RegionID"],
        "_private.electric_machines._1428": ["ResultsLocationsSpecification"],
        "_private.electric_machines._1429": ["Rotor"],
        "_private.electric_machines._1430": ["RotorInternalLayerSpecification"],
        "_private.electric_machines._1431": ["RotorSkewSlice"],
        "_private.electric_machines._1432": ["RotorType"],
        "_private.electric_machines._1433": ["SingleOrDoubleLayerWindings"],
        "_private.electric_machines._1434": ["SlotSectionDetail"],
        "_private.electric_machines._1435": ["Stator"],
        "_private.electric_machines._1436": ["StatorCutoutSpecification"],
        "_private.electric_machines._1437": ["StatorRotorMaterial"],
        "_private.electric_machines._1438": ["StatorRotorMaterialDatabase"],
        "_private.electric_machines._1439": ["SurfacePermanentMagnetMachine"],
        "_private.electric_machines._1440": ["SurfacePermanentMagnetRotor"],
        "_private.electric_machines._1441": ["SynchronousReluctanceMachine"],
        "_private.electric_machines._1442": ["ToothAndSlot"],
        "_private.electric_machines._1443": ["ToothSlotStyle"],
        "_private.electric_machines._1444": ["ToothTaperSpecification"],
        "_private.electric_machines._1445": ["TwoDimensionalFEModelForAnalysis"],
        "_private.electric_machines._1446": [
            "TwoDimensionalFEModelForElectromagneticAnalysis"
        ],
        "_private.electric_machines._1447": [
            "TwoDimensionalFEModelForMechanicalAnalysis"
        ],
        "_private.electric_machines._1448": ["UShapedLayerSpecification"],
        "_private.electric_machines._1449": ["VShapedMagnetLayerSpecification"],
        "_private.electric_machines._1450": ["WindingConductor"],
        "_private.electric_machines._1451": ["WindingConnection"],
        "_private.electric_machines._1452": ["WindingMaterial"],
        "_private.electric_machines._1453": ["WindingMaterialDatabase"],
        "_private.electric_machines._1454": ["Windings"],
        "_private.electric_machines._1455": ["WindingsViewer"],
        "_private.electric_machines._1456": ["WindingType"],
        "_private.electric_machines._1457": ["WireSizeSpecificationMethod"],
        "_private.electric_machines._1458": ["WoundFieldSynchronousMachine"],
        "_private.electric_machines._1459": ["WoundFieldSynchronousRotor"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractStator",
    "AbstractToothAndSlot",
    "CADConductor",
    "CADElectricMachineDetail",
    "CADFieldWindingSpecification",
    "CADMagnetDetails",
    "CADMagnetsForLayer",
    "CADRotor",
    "CADStator",
    "CADToothAndSlot",
    "CADWoundFieldSynchronousRotor",
    "Coil",
    "CoilPositionInSlot",
    "CoolingChannelShape",
    "CoolingDuctLayerSpecification",
    "CoolingDuctShape",
    "CoreLossBuildFactorSpecificationMethod",
    "CoreLossCoefficients",
    "DoubleLayerWindingSlotPositions",
    "DQAxisConvention",
    "Eccentricity",
    "ElectricMachineDesignBase",
    "ElectricMachineDetail",
    "ElectricMachineDetailInitialInformation",
    "ElectricMachineElectromagneticAndThermalMeshingOptions",
    "ElectricMachineGroup",
    "ElectricMachineMechanicalAnalysisMeshingOptions",
    "ElectricMachineMeshingOptions",
    "ElectricMachineMeshingOptionsBase",
    "ElectricMachineSetup",
    "ElectricMachineSetupBase",
    "ElectricMachineThermalMeshingOptions",
    "ElectricMachineType",
    "FieldWindingSpecification",
    "FieldWindingSpecificationBase",
    "FillFactorSpecificationMethod",
    "FluxBarriers",
    "FluxBarrierOrWeb",
    "FluxBarrierStyle",
    "GeneralElectricMachineMaterial",
    "GeneralElectricMachineMaterialDatabase",
    "HairpinConductor",
    "HarmonicLoadDataControlExcitationOptionForElectricMachineMode",
    "IndividualConductorSpecificationSource",
    "InteriorPermanentMagnetAndSynchronousReluctanceRotor",
    "InteriorPermanentMagnetMachine",
    "IronLossCoefficientSpecificationMethod",
    "MagnetClearance",
    "MagnetConfiguration",
    "MagnetData",
    "MagnetDesign",
    "MagnetForLayer",
    "MagnetisationDirection",
    "MagnetMaterial",
    "MagnetMaterialDatabase",
    "MotorRotorSideFaceDetail",
    "NonCADElectricMachineDetail",
    "NotchShape",
    "NotchSpecification",
    "PermanentMagnetAssistedSynchronousReluctanceMachine",
    "PermanentMagnetRotor",
    "Phase",
    "RegionID",
    "ResultsLocationsSpecification",
    "Rotor",
    "RotorInternalLayerSpecification",
    "RotorSkewSlice",
    "RotorType",
    "SingleOrDoubleLayerWindings",
    "SlotSectionDetail",
    "Stator",
    "StatorCutoutSpecification",
    "StatorRotorMaterial",
    "StatorRotorMaterialDatabase",
    "SurfacePermanentMagnetMachine",
    "SurfacePermanentMagnetRotor",
    "SynchronousReluctanceMachine",
    "ToothAndSlot",
    "ToothSlotStyle",
    "ToothTaperSpecification",
    "TwoDimensionalFEModelForAnalysis",
    "TwoDimensionalFEModelForElectromagneticAnalysis",
    "TwoDimensionalFEModelForMechanicalAnalysis",
    "UShapedLayerSpecification",
    "VShapedMagnetLayerSpecification",
    "WindingConductor",
    "WindingConnection",
    "WindingMaterial",
    "WindingMaterialDatabase",
    "Windings",
    "WindingsViewer",
    "WindingType",
    "WireSizeSpecificationMethod",
    "WoundFieldSynchronousMachine",
    "WoundFieldSynchronousRotor",
)
