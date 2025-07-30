"""DataScalingReferenceValues"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility.measured_data_scaling import _1755

_DATA_SCALING_REFERENCE_VALUES = python_net_import(
    "SMT.MastaAPI.MathUtility.MeasuredDataScaling", "DataScalingReferenceValues"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, Union

    from mastapy._private.utility.units_and_measurements import _1797

    Self = TypeVar("Self", bound="DataScalingReferenceValues")
    CastSelf = TypeVar(
        "CastSelf", bound="DataScalingReferenceValues._Cast_DataScalingReferenceValues"
    )

TMeasurement = TypeVar("TMeasurement", bound="_1797.MeasurementBase")

__docformat__ = "restructuredtext en"
__all__ = ("DataScalingReferenceValues",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DataScalingReferenceValues:
    """Special nested class for casting DataScalingReferenceValues to subclasses."""

    __parent__: "DataScalingReferenceValues"

    @property
    def data_scaling_reference_values_base(
        self: "CastSelf",
    ) -> "_1755.DataScalingReferenceValuesBase":
        return self.__parent__._cast(_1755.DataScalingReferenceValuesBase)

    @property
    def data_scaling_reference_values(self: "CastSelf") -> "DataScalingReferenceValues":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class DataScalingReferenceValues(
    _1755.DataScalingReferenceValuesBase, Generic[TMeasurement]
):
    """DataScalingReferenceValues

    This is a mastapy class.

    Generic Types:
        TMeasurement
    """

    TYPE: ClassVar["Type"] = _DATA_SCALING_REFERENCE_VALUES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def decibel_reference(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DecibelReference")

        if temp is None:
            return 0.0

        return temp

    @decibel_reference.setter
    @exception_bridge
    @enforce_parameter_types
    def decibel_reference(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DecibelReference", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def maximum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Maximum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Maximum", value)

    @property
    @exception_bridge
    def minimum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Minimum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Minimum", value)

    @property
    def cast_to(self: "Self") -> "_Cast_DataScalingReferenceValues":
        """Cast to another type.

        Returns:
            _Cast_DataScalingReferenceValues
        """
        return _Cast_DataScalingReferenceValues(self)
