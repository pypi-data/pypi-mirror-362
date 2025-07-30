"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.thermal._1460 import (
        AdditionalSliceSpecification,
    )
    from mastapy._private.electric_machines.thermal._1461 import Channel
    from mastapy._private.electric_machines.thermal._1462 import ComponentSetup
    from mastapy._private.electric_machines.thermal._1463 import (
        CoolingChannelForThermalAnalysis,
    )
    from mastapy._private.electric_machines.thermal._1464 import CoolingJacketType
    from mastapy._private.electric_machines.thermal._1465 import EdgeSelector
    from mastapy._private.electric_machines.thermal._1466 import (
        EndWindingCoolingFlowSource,
    )
    from mastapy._private.electric_machines.thermal._1467 import EndWindingLengthSource
    from mastapy._private.electric_machines.thermal._1468 import (
        EndWindingThermalElement,
    )
    from mastapy._private.electric_machines.thermal._1469 import (
        HeatTransferCoefficientCalculationMethod,
    )
    from mastapy._private.electric_machines.thermal._1470 import (
        HousingChannelModificationFactors,
    )
    from mastapy._private.electric_machines.thermal._1471 import HousingFlowDirection
    from mastapy._private.electric_machines.thermal._1472 import InitialInformation
    from mastapy._private.electric_machines.thermal._1473 import InletLocation
    from mastapy._private.electric_machines.thermal._1474 import (
        RegionIDForThermalAnalysis,
    )
    from mastapy._private.electric_machines.thermal._1475 import RotorSetup
    from mastapy._private.electric_machines.thermal._1476 import SliceLengthInformation
    from mastapy._private.electric_machines.thermal._1477 import (
        SliceLengthInformationPerRegion,
    )
    from mastapy._private.electric_machines.thermal._1478 import (
        SliceLengthInformationReporter,
    )
    from mastapy._private.electric_machines.thermal._1479 import StatorSetup
    from mastapy._private.electric_machines.thermal._1480 import ThermalElectricMachine
    from mastapy._private.electric_machines.thermal._1481 import (
        ThermalElectricMachineSetup,
    )
    from mastapy._private.electric_machines.thermal._1482 import ThermalEndcap
    from mastapy._private.electric_machines.thermal._1483 import ThermalEndWinding
    from mastapy._private.electric_machines.thermal._1484 import (
        ThermalEndWindingSurfaceCollection,
    )
    from mastapy._private.electric_machines.thermal._1485 import ThermalHousing
    from mastapy._private.electric_machines.thermal._1486 import ThermalRotor
    from mastapy._private.electric_machines.thermal._1487 import ThermalStator
    from mastapy._private.electric_machines.thermal._1488 import ThermalWindings
    from mastapy._private.electric_machines.thermal._1489 import (
        UserSpecifiedEdgeIndices,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.thermal._1460": ["AdditionalSliceSpecification"],
        "_private.electric_machines.thermal._1461": ["Channel"],
        "_private.electric_machines.thermal._1462": ["ComponentSetup"],
        "_private.electric_machines.thermal._1463": [
            "CoolingChannelForThermalAnalysis"
        ],
        "_private.electric_machines.thermal._1464": ["CoolingJacketType"],
        "_private.electric_machines.thermal._1465": ["EdgeSelector"],
        "_private.electric_machines.thermal._1466": ["EndWindingCoolingFlowSource"],
        "_private.electric_machines.thermal._1467": ["EndWindingLengthSource"],
        "_private.electric_machines.thermal._1468": ["EndWindingThermalElement"],
        "_private.electric_machines.thermal._1469": [
            "HeatTransferCoefficientCalculationMethod"
        ],
        "_private.electric_machines.thermal._1470": [
            "HousingChannelModificationFactors"
        ],
        "_private.electric_machines.thermal._1471": ["HousingFlowDirection"],
        "_private.electric_machines.thermal._1472": ["InitialInformation"],
        "_private.electric_machines.thermal._1473": ["InletLocation"],
        "_private.electric_machines.thermal._1474": ["RegionIDForThermalAnalysis"],
        "_private.electric_machines.thermal._1475": ["RotorSetup"],
        "_private.electric_machines.thermal._1476": ["SliceLengthInformation"],
        "_private.electric_machines.thermal._1477": ["SliceLengthInformationPerRegion"],
        "_private.electric_machines.thermal._1478": ["SliceLengthInformationReporter"],
        "_private.electric_machines.thermal._1479": ["StatorSetup"],
        "_private.electric_machines.thermal._1480": ["ThermalElectricMachine"],
        "_private.electric_machines.thermal._1481": ["ThermalElectricMachineSetup"],
        "_private.electric_machines.thermal._1482": ["ThermalEndcap"],
        "_private.electric_machines.thermal._1483": ["ThermalEndWinding"],
        "_private.electric_machines.thermal._1484": [
            "ThermalEndWindingSurfaceCollection"
        ],
        "_private.electric_machines.thermal._1485": ["ThermalHousing"],
        "_private.electric_machines.thermal._1486": ["ThermalRotor"],
        "_private.electric_machines.thermal._1487": ["ThermalStator"],
        "_private.electric_machines.thermal._1488": ["ThermalWindings"],
        "_private.electric_machines.thermal._1489": ["UserSpecifiedEdgeIndices"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdditionalSliceSpecification",
    "Channel",
    "ComponentSetup",
    "CoolingChannelForThermalAnalysis",
    "CoolingJacketType",
    "EdgeSelector",
    "EndWindingCoolingFlowSource",
    "EndWindingLengthSource",
    "EndWindingThermalElement",
    "HeatTransferCoefficientCalculationMethod",
    "HousingChannelModificationFactors",
    "HousingFlowDirection",
    "InitialInformation",
    "InletLocation",
    "RegionIDForThermalAnalysis",
    "RotorSetup",
    "SliceLengthInformation",
    "SliceLengthInformationPerRegion",
    "SliceLengthInformationReporter",
    "StatorSetup",
    "ThermalElectricMachine",
    "ThermalElectricMachineSetup",
    "ThermalEndcap",
    "ThermalEndWinding",
    "ThermalEndWindingSurfaceCollection",
    "ThermalHousing",
    "ThermalRotor",
    "ThermalStator",
    "ThermalWindings",
    "UserSpecifiedEdgeIndices",
)
