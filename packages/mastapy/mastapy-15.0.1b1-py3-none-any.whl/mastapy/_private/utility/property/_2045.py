"""DutyCyclePropertySummaryVeryShortLength"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.utility.property import _2040
from mastapy._private.utility.units_and_measurements.measurements import _1908

_DUTY_CYCLE_PROPERTY_SUMMARY_VERY_SHORT_LENGTH = python_net_import(
    "SMT.MastaAPI.Utility.Property", "DutyCyclePropertySummaryVeryShortLength"
)

if TYPE_CHECKING:
    from typing import Any, Type

    Self = TypeVar("Self", bound="DutyCyclePropertySummaryVeryShortLength")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DutyCyclePropertySummaryVeryShortLength._Cast_DutyCyclePropertySummaryVeryShortLength",
    )

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("DutyCyclePropertySummaryVeryShortLength",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DutyCyclePropertySummaryVeryShortLength:
    """Special nested class for casting DutyCyclePropertySummaryVeryShortLength to subclasses."""

    __parent__: "DutyCyclePropertySummaryVeryShortLength"

    @property
    def duty_cycle_property_summary(
        self: "CastSelf",
    ) -> "_2040.DutyCyclePropertySummary":
        return self.__parent__._cast(_2040.DutyCyclePropertySummary)

    @property
    def duty_cycle_property_summary_very_short_length(
        self: "CastSelf",
    ) -> "DutyCyclePropertySummaryVeryShortLength":
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
class DutyCyclePropertySummaryVeryShortLength(
    _2040.DutyCyclePropertySummary[_1908.Stress, T]
):
    """DutyCyclePropertySummaryVeryShortLength

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _DUTY_CYCLE_PROPERTY_SUMMARY_VERY_SHORT_LENGTH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def average_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageValue")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumValue")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumValue")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_DutyCyclePropertySummaryVeryShortLength":
        """Cast to another type.

        Returns:
            _Cast_DutyCyclePropertySummaryVeryShortLength
        """
        return _Cast_DutyCyclePropertySummaryVeryShortLength(self)
