"""DutyCyclePropertySummary"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_DUTY_CYCLE_PROPERTY_SUMMARY = python_net_import(
    "SMT.MastaAPI.Utility.Property", "DutyCyclePropertySummary"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.utility.property import _2041, _2042, _2043, _2044, _2045
    from mastapy._private.utility.units_and_measurements import _1797

    Self = TypeVar("Self", bound="DutyCyclePropertySummary")
    CastSelf = TypeVar(
        "CastSelf", bound="DutyCyclePropertySummary._Cast_DutyCyclePropertySummary"
    )

TMeasurement = TypeVar("TMeasurement", bound="_1797.MeasurementBase")
T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("DutyCyclePropertySummary",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DutyCyclePropertySummary:
    """Special nested class for casting DutyCyclePropertySummary to subclasses."""

    __parent__: "DutyCyclePropertySummary"

    @property
    def duty_cycle_property_summary_force(
        self: "CastSelf",
    ) -> "_2041.DutyCyclePropertySummaryForce":
        from mastapy._private.utility.property import _2041

        return self.__parent__._cast(_2041.DutyCyclePropertySummaryForce)

    @property
    def duty_cycle_property_summary_percentage(
        self: "CastSelf",
    ) -> "_2042.DutyCyclePropertySummaryPercentage":
        from mastapy._private.utility.property import _2042

        return self.__parent__._cast(_2042.DutyCyclePropertySummaryPercentage)

    @property
    def duty_cycle_property_summary_small_angle(
        self: "CastSelf",
    ) -> "_2043.DutyCyclePropertySummarySmallAngle":
        from mastapy._private.utility.property import _2043

        return self.__parent__._cast(_2043.DutyCyclePropertySummarySmallAngle)

    @property
    def duty_cycle_property_summary_stress(
        self: "CastSelf",
    ) -> "_2044.DutyCyclePropertySummaryStress":
        from mastapy._private.utility.property import _2044

        return self.__parent__._cast(_2044.DutyCyclePropertySummaryStress)

    @property
    def duty_cycle_property_summary_very_short_length(
        self: "CastSelf",
    ) -> "_2045.DutyCyclePropertySummaryVeryShortLength":
        from mastapy._private.utility.property import _2045

        return self.__parent__._cast(_2045.DutyCyclePropertySummaryVeryShortLength)

    @property
    def duty_cycle_property_summary(self: "CastSelf") -> "DutyCyclePropertySummary":
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
class DutyCyclePropertySummary(_0.APIBase, Generic[TMeasurement, T]):
    """DutyCyclePropertySummary

    This is a mastapy class.

    Generic Types:
        TMeasurement
        T
    """

    TYPE: ClassVar["Type"] = _DUTY_CYCLE_PROPERTY_SUMMARY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_absolute_value_load_case(self: "Self") -> "T":
        """T

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumAbsoluteValueLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def maximum_value_load_case(self: "Self") -> "T":
        """T

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumValueLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minimum_value_load_case(self: "Self") -> "T":
        """T

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumValueLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_DutyCyclePropertySummary":
        """Cast to another type.

        Returns:
            _Cast_DutyCyclePropertySummary
        """
        return _Cast_DutyCyclePropertySummary(self)
