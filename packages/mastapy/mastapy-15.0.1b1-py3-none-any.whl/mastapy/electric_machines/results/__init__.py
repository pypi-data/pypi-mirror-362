"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.results._1505 import DynamicForceResults
    from mastapy._private.electric_machines.results._1506 import EfficiencyResults
    from mastapy._private.electric_machines.results._1507 import ElectricMachineDQModel
    from mastapy._private.electric_machines.results._1508 import (
        ElectricMachineMechanicalResults,
    )
    from mastapy._private.electric_machines.results._1509 import (
        ElectricMachineMechanicalResultsViewable,
    )
    from mastapy._private.electric_machines.results._1510 import ElectricMachineResults
    from mastapy._private.electric_machines.results._1511 import (
        ElectricMachineResultsForConductorTurn,
    )
    from mastapy._private.electric_machines.results._1512 import (
        ElectricMachineResultsForConductorTurnAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1513 import (
        ElectricMachineResultsForLineToLine,
    )
    from mastapy._private.electric_machines.results._1514 import (
        ElectricMachineResultsForOpenCircuitAndOnLoad,
    )
    from mastapy._private.electric_machines.results._1515 import (
        ElectricMachineResultsForPhase,
    )
    from mastapy._private.electric_machines.results._1516 import (
        ElectricMachineResultsForPhaseAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1517 import (
        ElectricMachineResultsForStatorToothAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1518 import (
        ElectricMachineResultsLineToLineAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1519 import (
        ElectricMachineResultsTimeStep,
    )
    from mastapy._private.electric_machines.results._1520 import (
        ElectricMachineResultsTimeStepAtLocation,
    )
    from mastapy._private.electric_machines.results._1521 import (
        ElectricMachineResultsViewable,
    )
    from mastapy._private.electric_machines.results._1522 import (
        ElectricMachineForceViewOptions,
    )
    from mastapy._private.electric_machines.results._1524 import LinearDQModel
    from mastapy._private.electric_machines.results._1525 import (
        MaximumTorqueResultsPoints,
    )
    from mastapy._private.electric_machines.results._1526 import NonLinearDQModel
    from mastapy._private.electric_machines.results._1527 import (
        NonLinearDQModelGeneratorSettings,
    )
    from mastapy._private.electric_machines.results._1528 import (
        OnLoadElectricMachineResults,
    )
    from mastapy._private.electric_machines.results._1529 import (
        OpenCircuitElectricMachineResults,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.results._1505": ["DynamicForceResults"],
        "_private.electric_machines.results._1506": ["EfficiencyResults"],
        "_private.electric_machines.results._1507": ["ElectricMachineDQModel"],
        "_private.electric_machines.results._1508": [
            "ElectricMachineMechanicalResults"
        ],
        "_private.electric_machines.results._1509": [
            "ElectricMachineMechanicalResultsViewable"
        ],
        "_private.electric_machines.results._1510": ["ElectricMachineResults"],
        "_private.electric_machines.results._1511": [
            "ElectricMachineResultsForConductorTurn"
        ],
        "_private.electric_machines.results._1512": [
            "ElectricMachineResultsForConductorTurnAtTimeStep"
        ],
        "_private.electric_machines.results._1513": [
            "ElectricMachineResultsForLineToLine"
        ],
        "_private.electric_machines.results._1514": [
            "ElectricMachineResultsForOpenCircuitAndOnLoad"
        ],
        "_private.electric_machines.results._1515": ["ElectricMachineResultsForPhase"],
        "_private.electric_machines.results._1516": [
            "ElectricMachineResultsForPhaseAtTimeStep"
        ],
        "_private.electric_machines.results._1517": [
            "ElectricMachineResultsForStatorToothAtTimeStep"
        ],
        "_private.electric_machines.results._1518": [
            "ElectricMachineResultsLineToLineAtTimeStep"
        ],
        "_private.electric_machines.results._1519": ["ElectricMachineResultsTimeStep"],
        "_private.electric_machines.results._1520": [
            "ElectricMachineResultsTimeStepAtLocation"
        ],
        "_private.electric_machines.results._1521": ["ElectricMachineResultsViewable"],
        "_private.electric_machines.results._1522": ["ElectricMachineForceViewOptions"],
        "_private.electric_machines.results._1524": ["LinearDQModel"],
        "_private.electric_machines.results._1525": ["MaximumTorqueResultsPoints"],
        "_private.electric_machines.results._1526": ["NonLinearDQModel"],
        "_private.electric_machines.results._1527": [
            "NonLinearDQModelGeneratorSettings"
        ],
        "_private.electric_machines.results._1528": ["OnLoadElectricMachineResults"],
        "_private.electric_machines.results._1529": [
            "OpenCircuitElectricMachineResults"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DynamicForceResults",
    "EfficiencyResults",
    "ElectricMachineDQModel",
    "ElectricMachineMechanicalResults",
    "ElectricMachineMechanicalResultsViewable",
    "ElectricMachineResults",
    "ElectricMachineResultsForConductorTurn",
    "ElectricMachineResultsForConductorTurnAtTimeStep",
    "ElectricMachineResultsForLineToLine",
    "ElectricMachineResultsForOpenCircuitAndOnLoad",
    "ElectricMachineResultsForPhase",
    "ElectricMachineResultsForPhaseAtTimeStep",
    "ElectricMachineResultsForStatorToothAtTimeStep",
    "ElectricMachineResultsLineToLineAtTimeStep",
    "ElectricMachineResultsTimeStep",
    "ElectricMachineResultsTimeStepAtLocation",
    "ElectricMachineResultsViewable",
    "ElectricMachineForceViewOptions",
    "LinearDQModel",
    "MaximumTorqueResultsPoints",
    "NonLinearDQModel",
    "NonLinearDQModelGeneratorSettings",
    "OnLoadElectricMachineResults",
    "OpenCircuitElectricMachineResults",
)
