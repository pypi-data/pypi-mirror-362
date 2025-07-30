"""MeasurementTypeExtensions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_MEASUREMENT_TYPE_EXTENSIONS = python_net_import(
    "SMT.MastaAPIUtility.UnitsAndMeasurements", "MeasurementTypeExtensions"
)

if TYPE_CHECKING:
    from typing import Any, NoReturn, Type

    from mastapy._private.units_and_measurements import _7903


__docformat__ = "restructuredtext en"
__all__ = ("MeasurementTypeExtensions",)


class MeasurementTypeExtensions:
    """MeasurementTypeExtensions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MEASUREMENT_TYPE_EXTENSIONS

    def __new__(
        cls: "Type[MeasurementTypeExtensions]", *args: "Any", **kwargs: "Any"
    ) -> "NoReturn":
        """Override of the new magic method.

        Note:
            This class cannot be instantiated and this method will always throw an
            exception.

        Args:
            cls (Type[MeasurementTypeExtensions]: The class to instantiate.
            *args (Any): Arguments.
            **kwargs (Any): Keyword arguments.

        Returns:
            NoReturn
        """
        raise TypeError("Class cannot be instantiated. Please use statically.")

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def is_unmeasurable(measurement_type: "_7903.MeasurementType") -> "bool":
        """bool

        Args:
            measurement_type (mastapy.units_and_measurements.MeasurementType)
        """
        measurement_type = conversion.mp_to_pn_enum(
            measurement_type, "SMT.MastaAPIUtility.UnitsAndMeasurements.MeasurementType"
        )
        method_result = pythonnet_method_call(
            MeasurementTypeExtensions.TYPE, "IsUnmeasurable", measurement_type
        )
        return method_result

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def is_angle(measurement_type: "_7903.MeasurementType") -> "bool":
        """bool

        Args:
            measurement_type (mastapy.units_and_measurements.MeasurementType)
        """
        measurement_type = conversion.mp_to_pn_enum(
            measurement_type, "SMT.MastaAPIUtility.UnitsAndMeasurements.MeasurementType"
        )
        method_result = pythonnet_method_call(
            MeasurementTypeExtensions.TYPE, "IsAngle", measurement_type
        )
        return method_result

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def is_root_power_quantity(measurement_type: "_7903.MeasurementType") -> "bool":
        """bool

        Args:
            measurement_type (mastapy.units_and_measurements.MeasurementType)
        """
        measurement_type = conversion.mp_to_pn_enum(
            measurement_type, "SMT.MastaAPIUtility.UnitsAndMeasurements.MeasurementType"
        )
        method_result = pythonnet_method_call(
            MeasurementTypeExtensions.TYPE, "IsRootPowerQuantity", measurement_type
        )
        return method_result
