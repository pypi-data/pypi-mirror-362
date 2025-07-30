"""DataScalingReferenceValuesBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_DATA_SCALING_REFERENCE_VALUES_BASE = python_net_import(
    "SMT.MastaAPI.MathUtility.MeasuredDataScaling", "DataScalingReferenceValuesBase"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility.measured_data_scaling import _1754

    Self = TypeVar("Self", bound="DataScalingReferenceValuesBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DataScalingReferenceValuesBase._Cast_DataScalingReferenceValuesBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DataScalingReferenceValuesBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DataScalingReferenceValuesBase:
    """Special nested class for casting DataScalingReferenceValuesBase to subclasses."""

    __parent__: "DataScalingReferenceValuesBase"

    @property
    def data_scaling_reference_values(
        self: "CastSelf",
    ) -> "_1754.DataScalingReferenceValues":
        from mastapy._private.math_utility.measured_data_scaling import _1754

        return self.__parent__._cast(_1754.DataScalingReferenceValues)

    @property
    def data_scaling_reference_values_base(
        self: "CastSelf",
    ) -> "DataScalingReferenceValuesBase":
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
class DataScalingReferenceValuesBase(_0.APIBase):
    """DataScalingReferenceValuesBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATA_SCALING_REFERENCE_VALUES_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_db(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumDB")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_db.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_db(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumDB", value)

    @property
    @exception_bridge
    def minimum_db(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumDB")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_db.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_db(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumDB", value)

    @property
    def cast_to(self: "Self") -> "_Cast_DataScalingReferenceValuesBase":
        """Cast to another type.

        Returns:
            _Cast_DataScalingReferenceValuesBase
        """
        return _Cast_DataScalingReferenceValuesBase(self)
