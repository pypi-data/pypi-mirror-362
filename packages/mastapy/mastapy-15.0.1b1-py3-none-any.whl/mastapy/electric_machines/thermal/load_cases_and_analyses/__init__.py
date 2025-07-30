"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1496 import (
        CoolingLoadCaseSettings,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1497 import (
        HeatDissipationReporter,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1498 import (
        HeatFlowReporter,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1499 import (
        HeatTransferCoefficientReporter,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1500 import (
        PowerLosses,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1501 import (
        PressureDropReporter,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1502 import (
        ThermalAnalysis,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1503 import (
        ThermalLoadCase,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1504 import (
        ThermalLoadCaseGroup,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.thermal.load_cases_and_analyses._1496": [
            "CoolingLoadCaseSettings"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1497": [
            "HeatDissipationReporter"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1498": [
            "HeatFlowReporter"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1499": [
            "HeatTransferCoefficientReporter"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1500": [
            "PowerLosses"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1501": [
            "PressureDropReporter"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1502": [
            "ThermalAnalysis"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1503": [
            "ThermalLoadCase"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1504": [
            "ThermalLoadCaseGroup"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CoolingLoadCaseSettings",
    "HeatDissipationReporter",
    "HeatFlowReporter",
    "HeatTransferCoefficientReporter",
    "PowerLosses",
    "PressureDropReporter",
    "ThermalAnalysis",
    "ThermalLoadCase",
    "ThermalLoadCaseGroup",
)
