"""ShaftSafetyFactorSettings"""

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

_SHAFT_SAFETY_FACTOR_SETTINGS = python_net_import(
    "SMT.MastaAPI.Shafts", "ShaftSafetyFactorSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShaftSafetyFactorSettings")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftSafetyFactorSettings._Cast_ShaftSafetyFactorSettings"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSafetyFactorSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSafetyFactorSettings:
    """Special nested class for casting ShaftSafetyFactorSettings to subclasses."""

    __parent__: "ShaftSafetyFactorSettings"

    @property
    def shaft_safety_factor_settings(self: "CastSelf") -> "ShaftSafetyFactorSettings":
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
class ShaftSafetyFactorSettings(_0.APIBase):
    """ShaftSafetyFactorSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SAFETY_FACTOR_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def shaft_fatigue_safety_factor_requirement(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ShaftFatigueSafetyFactorRequirement"
        )

        if temp is None:
            return 0.0

        return temp

    @shaft_fatigue_safety_factor_requirement.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_fatigue_safety_factor_requirement(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaftFatigueSafetyFactorRequirement",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shaft_static_safety_factor_requirement(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ShaftStaticSafetyFactorRequirement"
        )

        if temp is None:
            return 0.0

        return temp

    @shaft_static_safety_factor_requirement.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_static_safety_factor_requirement(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaftStaticSafetyFactorRequirement",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSafetyFactorSettings":
        """Cast to another type.

        Returns:
            _Cast_ShaftSafetyFactorSettings
        """
        return _Cast_ShaftSafetyFactorSettings(self)
