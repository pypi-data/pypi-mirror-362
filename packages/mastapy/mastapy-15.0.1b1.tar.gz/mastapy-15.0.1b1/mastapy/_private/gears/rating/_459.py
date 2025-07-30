"""SafetyFactorResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_SAFETY_FACTOR_RESULTS = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "SafetyFactorResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SafetyFactorResults")
    CastSelf = TypeVar(
        "CastSelf", bound="SafetyFactorResults._Cast_SafetyFactorResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SafetyFactorResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SafetyFactorResults:
    """Special nested class for casting SafetyFactorResults to subclasses."""

    __parent__: "SafetyFactorResults"

    @property
    def safety_factor_results(self: "CastSelf") -> "SafetyFactorResults":
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
class SafetyFactorResults(_0.APIBase):
    """SafetyFactorResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SAFETY_FACTOR_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fatigue_bending_safety_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FatigueBendingSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @fatigue_bending_safety_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def fatigue_bending_safety_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FatigueBendingSafetyFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def fatigue_contact_safety_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FatigueContactSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @fatigue_contact_safety_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def fatigue_contact_safety_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FatigueContactSafetyFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def fatigue_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def static_bending_safety_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StaticBendingSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @static_bending_safety_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def static_bending_safety_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StaticBendingSafetyFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def static_contact_safety_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StaticContactSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @static_contact_safety_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def static_contact_safety_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StaticContactSafetyFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def static_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SafetyFactorResults":
        """Cast to another type.

        Returns:
            _Cast_SafetyFactorResults
        """
        return _Cast_SafetyFactorResults(self)
