"""MultipleFourierSeriesInterpolator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_MULTIPLE_FOURIER_SERIES_INTERPOLATOR = python_net_import(
    "SMT.MastaAPI.MathUtility", "MultipleFourierSeriesInterpolator"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1697

    Self = TypeVar("Self", bound="MultipleFourierSeriesInterpolator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MultipleFourierSeriesInterpolator._Cast_MultipleFourierSeriesInterpolator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MultipleFourierSeriesInterpolator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MultipleFourierSeriesInterpolator:
    """Special nested class for casting MultipleFourierSeriesInterpolator to subclasses."""

    __parent__: "MultipleFourierSeriesInterpolator"

    @property
    def multiple_fourier_series_interpolator(
        self: "CastSelf",
    ) -> "MultipleFourierSeriesInterpolator":
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
class MultipleFourierSeriesInterpolator(_0.APIBase):
    """MultipleFourierSeriesInterpolator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MULTIPLE_FOURIER_SERIES_INTERPOLATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def x_values_where_data_has_been_specified(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XValuesWhereDataHasBeenSpecified")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def fourier_series_for(self: "Self", x_value: "float") -> "_1697.FourierSeries":
        """mastapy.math_utility.FourierSeries

        Args:
            x_value (float)
        """
        x_value = float(x_value)
        method_result = pythonnet_method_call(
            self.wrapped, "FourierSeriesFor", x_value if x_value else 0.0
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def remove_fourier_series_at(self: "Self", x_value: "float") -> None:
        """Method does not return.

        Args:
            x_value (float)
        """
        x_value = float(x_value)
        pythonnet_method_call(
            self.wrapped, "RemoveFourierSeriesAt", x_value if x_value else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MultipleFourierSeriesInterpolator":
        """Cast to another type.

        Returns:
            _Cast_MultipleFourierSeriesInterpolator
        """
        return _Cast_MultipleFourierSeriesInterpolator(self)
