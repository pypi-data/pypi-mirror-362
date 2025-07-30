"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2793 import (
        BoostPressureInputOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2794 import (
        InputPowerInputOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2795 import (
        PressureRatioInputOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2796 import (
        RotorSetDataInputFileOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2797 import (
        RotorSetMeasuredPoint,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2798 import (
        RotorSpeedInputOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2799 import (
        SuperchargerMap,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2800 import (
        SuperchargerMaps,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2801 import (
        SuperchargerRotorSet,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2802 import (
        SuperchargerRotorSetDatabase,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2803 import (
        YVariableForImportedData,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.gears.supercharger_rotor_set._2793": [
            "BoostPressureInputOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2794": [
            "InputPowerInputOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2795": [
            "PressureRatioInputOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2796": [
            "RotorSetDataInputFileOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2797": [
            "RotorSetMeasuredPoint"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2798": [
            "RotorSpeedInputOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2799": [
            "SuperchargerMap"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2800": [
            "SuperchargerMaps"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2801": [
            "SuperchargerRotorSet"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2802": [
            "SuperchargerRotorSetDatabase"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2803": [
            "YVariableForImportedData"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BoostPressureInputOptions",
    "InputPowerInputOptions",
    "PressureRatioInputOptions",
    "RotorSetDataInputFileOptions",
    "RotorSetMeasuredPoint",
    "RotorSpeedInputOptions",
    "SuperchargerMap",
    "SuperchargerMaps",
    "SuperchargerRotorSet",
    "SuperchargerRotorSetDatabase",
    "YVariableForImportedData",
)
