"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.load_cases_and_analyses._1530 import (
        BasicDynamicForceLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1531 import (
        DynamicForceAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1532 import (
        DynamicForceLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1533 import (
        DynamicForcesOperatingPoint,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1534 import (
        EfficiencyMapAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1535 import (
        EfficiencyMapLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1536 import (
        ElectricMachineAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1537 import (
        ElectricMachineBasicMechanicalLossSettings,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1538 import (
        ElectricMachineControlStrategy,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1539 import (
        ElectricMachineEfficiencyMapSettings,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1540 import (
        ElectricMachineFEAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1541 import (
        ElectricMachineFEMechanicalAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1542 import (
        ElectricMachineLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1543 import (
        ElectricMachineLoadCaseBase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1544 import (
        ElectricMachineLoadCaseGroup,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1545 import (
        ElectricMachineMechanicalLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1546 import (
        EndWindingInductanceMethod,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1547 import (
        LeadingOrLagging,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1548 import (
        LoadCaseType,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1549 import (
        LoadCaseTypeSelector,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1550 import (
        MotoringOrGenerating,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1551 import (
        NonLinearDQModelMultipleOperatingPointsLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1552 import (
        NumberOfStepsPerOperatingPointSpecificationMethod,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1553 import (
        OperatingPointsSpecificationMethod,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1554 import (
        SingleOperatingPointAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1555 import (
        SlotDetailForAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1556 import (
        SpecifyTorqueOrCurrent,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1557 import (
        SpeedPointsDistribution,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1558 import (
        SpeedTorqueCurveAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1559 import (
        SpeedTorqueCurveLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1560 import (
        SpeedTorqueLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1561 import (
        Temperatures,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.load_cases_and_analyses._1530": [
            "BasicDynamicForceLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1531": [
            "DynamicForceAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1532": [
            "DynamicForceLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1533": [
            "DynamicForcesOperatingPoint"
        ],
        "_private.electric_machines.load_cases_and_analyses._1534": [
            "EfficiencyMapAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1535": [
            "EfficiencyMapLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1536": [
            "ElectricMachineAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1537": [
            "ElectricMachineBasicMechanicalLossSettings"
        ],
        "_private.electric_machines.load_cases_and_analyses._1538": [
            "ElectricMachineControlStrategy"
        ],
        "_private.electric_machines.load_cases_and_analyses._1539": [
            "ElectricMachineEfficiencyMapSettings"
        ],
        "_private.electric_machines.load_cases_and_analyses._1540": [
            "ElectricMachineFEAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1541": [
            "ElectricMachineFEMechanicalAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1542": [
            "ElectricMachineLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1543": [
            "ElectricMachineLoadCaseBase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1544": [
            "ElectricMachineLoadCaseGroup"
        ],
        "_private.electric_machines.load_cases_and_analyses._1545": [
            "ElectricMachineMechanicalLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1546": [
            "EndWindingInductanceMethod"
        ],
        "_private.electric_machines.load_cases_and_analyses._1547": [
            "LeadingOrLagging"
        ],
        "_private.electric_machines.load_cases_and_analyses._1548": ["LoadCaseType"],
        "_private.electric_machines.load_cases_and_analyses._1549": [
            "LoadCaseTypeSelector"
        ],
        "_private.electric_machines.load_cases_and_analyses._1550": [
            "MotoringOrGenerating"
        ],
        "_private.electric_machines.load_cases_and_analyses._1551": [
            "NonLinearDQModelMultipleOperatingPointsLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1552": [
            "NumberOfStepsPerOperatingPointSpecificationMethod"
        ],
        "_private.electric_machines.load_cases_and_analyses._1553": [
            "OperatingPointsSpecificationMethod"
        ],
        "_private.electric_machines.load_cases_and_analyses._1554": [
            "SingleOperatingPointAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1555": [
            "SlotDetailForAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1556": [
            "SpecifyTorqueOrCurrent"
        ],
        "_private.electric_machines.load_cases_and_analyses._1557": [
            "SpeedPointsDistribution"
        ],
        "_private.electric_machines.load_cases_and_analyses._1558": [
            "SpeedTorqueCurveAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1559": [
            "SpeedTorqueCurveLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1560": [
            "SpeedTorqueLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1561": ["Temperatures"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BasicDynamicForceLoadCase",
    "DynamicForceAnalysis",
    "DynamicForceLoadCase",
    "DynamicForcesOperatingPoint",
    "EfficiencyMapAnalysis",
    "EfficiencyMapLoadCase",
    "ElectricMachineAnalysis",
    "ElectricMachineBasicMechanicalLossSettings",
    "ElectricMachineControlStrategy",
    "ElectricMachineEfficiencyMapSettings",
    "ElectricMachineFEAnalysis",
    "ElectricMachineFEMechanicalAnalysis",
    "ElectricMachineLoadCase",
    "ElectricMachineLoadCaseBase",
    "ElectricMachineLoadCaseGroup",
    "ElectricMachineMechanicalLoadCase",
    "EndWindingInductanceMethod",
    "LeadingOrLagging",
    "LoadCaseType",
    "LoadCaseTypeSelector",
    "MotoringOrGenerating",
    "NonLinearDQModelMultipleOperatingPointsLoadCase",
    "NumberOfStepsPerOperatingPointSpecificationMethod",
    "OperatingPointsSpecificationMethod",
    "SingleOperatingPointAnalysis",
    "SlotDetailForAnalysis",
    "SpecifyTorqueOrCurrent",
    "SpeedPointsDistribution",
    "SpeedTorqueCurveAnalysis",
    "SpeedTorqueCurveLoadCase",
    "SpeedTorqueLoadCase",
    "Temperatures",
)
