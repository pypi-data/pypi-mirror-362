"""GearFlankRating"""

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
)

_GEAR_FLANK_RATING = python_net_import("SMT.MastaAPI.Gears.Rating", "GearFlankRating")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical import _547, _548

    Self = TypeVar("Self", bound="GearFlankRating")
    CastSelf = TypeVar("CastSelf", bound="GearFlankRating._Cast_GearFlankRating")


__docformat__ = "restructuredtext en"
__all__ = ("GearFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearFlankRating:
    """Special nested class for casting GearFlankRating to subclasses."""

    __parent__: "GearFlankRating"

    @property
    def cylindrical_gear_flank_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_547.CylindricalGearFlankDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _547

        return self.__parent__._cast(_547.CylindricalGearFlankDutyCycleRating)

    @property
    def cylindrical_gear_flank_rating(
        self: "CastSelf",
    ) -> "_548.CylindricalGearFlankRating":
        from mastapy._private.gears.rating.cylindrical import _548

        return self.__parent__._cast(_548.CylindricalGearFlankRating)

    @property
    def gear_flank_rating(self: "CastSelf") -> "GearFlankRating":
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
class GearFlankRating(_0.APIBase):
    """GearFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bending_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bending_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingSafetyFactorForStatic")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactSafetyFactorForStatic")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cycles(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cycles")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def damage_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def damage_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_static_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumStaticBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_static_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumStaticContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reliability_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReliabilityBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reliability_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReliabilityContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GearFlankRating":
        """Cast to another type.

        Returns:
            _Cast_GearFlankRating
        """
        return _Cast_GearFlankRating(self)
