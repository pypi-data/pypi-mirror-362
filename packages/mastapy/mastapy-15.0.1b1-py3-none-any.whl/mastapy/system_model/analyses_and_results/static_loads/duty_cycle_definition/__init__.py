"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7860 import (
        AdditionalForcesObtainedFrom,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7861 import (
        BoostPressureLoadCaseInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7862 import (
        DesignStateOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7863 import (
        DestinationDesignState,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7864 import (
        ForceInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7865 import (
        GearRatioInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7866 import (
        LoadCaseNameOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7867 import (
        MomentInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7868 import (
        MultiTimeSeriesDataInputFileOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7869 import (
        PointLoadInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7870 import (
        PowerLoadInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7871 import (
        RampOrSteadyStateInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7872 import (
        SpeedInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7873 import (
        TimeSeriesImporter,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7874 import (
        TimeStepInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7875 import (
        TorqueInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7876 import (
        TorqueValuesObtainedFrom,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7860": [
            "AdditionalForcesObtainedFrom"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7861": [
            "BoostPressureLoadCaseInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7862": [
            "DesignStateOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7863": [
            "DestinationDesignState"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7864": [
            "ForceInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7865": [
            "GearRatioInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7866": [
            "LoadCaseNameOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7867": [
            "MomentInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7868": [
            "MultiTimeSeriesDataInputFileOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7869": [
            "PointLoadInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7870": [
            "PowerLoadInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7871": [
            "RampOrSteadyStateInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7872": [
            "SpeedInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7873": [
            "TimeSeriesImporter"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7874": [
            "TimeStepInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7875": [
            "TorqueInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7876": [
            "TorqueValuesObtainedFrom"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdditionalForcesObtainedFrom",
    "BoostPressureLoadCaseInputOptions",
    "DesignStateOptions",
    "DestinationDesignState",
    "ForceInputOptions",
    "GearRatioInputOptions",
    "LoadCaseNameOptions",
    "MomentInputOptions",
    "MultiTimeSeriesDataInputFileOptions",
    "PointLoadInputOptions",
    "PowerLoadInputOptions",
    "RampOrSteadyStateInputOptions",
    "SpeedInputOptions",
    "TimeSeriesImporter",
    "TimeStepInputOptions",
    "TorqueInputOptions",
    "TorqueValuesObtainedFrom",
)
