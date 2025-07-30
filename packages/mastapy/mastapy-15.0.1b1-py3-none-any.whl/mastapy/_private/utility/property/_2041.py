"""DutyCyclePropertySummaryForce"""

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
from mastapy._private.utility.units_and_measurements.measurements import _1835

_DUTY_CYCLE_PROPERTY_SUMMARY_FORCE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "DutyCyclePropertySummaryForce"
)

if TYPE_CHECKING:
    from typing import Any, Type

    Self = TypeVar("Self", bound="DutyCyclePropertySummaryForce")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DutyCyclePropertySummaryForce._Cast_DutyCyclePropertySummaryForce",
    )

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("DutyCyclePropertySummaryForce",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DutyCyclePropertySummaryForce:
    """Special nested class for casting DutyCyclePropertySummaryForce to subclasses."""

    __parent__: "DutyCyclePropertySummaryForce"

    @property
    def duty_cycle_property_summary(
        self: "CastSelf",
    ) -> "_2040.DutyCyclePropertySummary":
        return self.__parent__._cast(_2040.DutyCyclePropertySummary)

    @property
    def duty_cycle_property_summary_force(
        self: "CastSelf",
    ) -> "DutyCyclePropertySummaryForce":
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
class DutyCyclePropertySummaryForce(_2040.DutyCyclePropertySummary[_1835.Force, T]):
    """DutyCyclePropertySummaryForce

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _DUTY_CYCLE_PROPERTY_SUMMARY_FORCE

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
    def maximum_absolute_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumAbsoluteValue")

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
    def cast_to(self: "Self") -> "_Cast_DutyCyclePropertySummaryForce":
        """Cast to another type.

        Returns:
            _Cast_DutyCyclePropertySummaryForce
        """
        return _Cast_DutyCyclePropertySummaryForce(self)
