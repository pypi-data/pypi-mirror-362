"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.units_and_measurements._1794 import (
        DegreesMinutesSeconds,
    )
    from mastapy._private.utility.units_and_measurements._1795 import EnumUnit
    from mastapy._private.utility.units_and_measurements._1796 import InverseUnit
    from mastapy._private.utility.units_and_measurements._1797 import MeasurementBase
    from mastapy._private.utility.units_and_measurements._1798 import (
        MeasurementSettings,
    )
    from mastapy._private.utility.units_and_measurements._1799 import MeasurementSystem
    from mastapy._private.utility.units_and_measurements._1800 import SafetyFactorUnit
    from mastapy._private.utility.units_and_measurements._1801 import TimeUnit
    from mastapy._private.utility.units_and_measurements._1802 import Unit
    from mastapy._private.utility.units_and_measurements._1803 import UnitGradient
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.units_and_measurements._1794": ["DegreesMinutesSeconds"],
        "_private.utility.units_and_measurements._1795": ["EnumUnit"],
        "_private.utility.units_and_measurements._1796": ["InverseUnit"],
        "_private.utility.units_and_measurements._1797": ["MeasurementBase"],
        "_private.utility.units_and_measurements._1798": ["MeasurementSettings"],
        "_private.utility.units_and_measurements._1799": ["MeasurementSystem"],
        "_private.utility.units_and_measurements._1800": ["SafetyFactorUnit"],
        "_private.utility.units_and_measurements._1801": ["TimeUnit"],
        "_private.utility.units_and_measurements._1802": ["Unit"],
        "_private.utility.units_and_measurements._1803": ["UnitGradient"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DegreesMinutesSeconds",
    "EnumUnit",
    "InverseUnit",
    "MeasurementBase",
    "MeasurementSettings",
    "MeasurementSystem",
    "SafetyFactorUnit",
    "TimeUnit",
    "Unit",
    "UnitGradient",
)
