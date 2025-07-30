"""SAESplineJointDutyCycleRating"""

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

_SAE_SPLINE_JOINT_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.DutyCycleRatings",
    "SAESplineJointDutyCycleRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SAESplineJointDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SAESplineJointDutyCycleRating._Cast_SAESplineJointDutyCycleRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SAESplineJointDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SAESplineJointDutyCycleRating:
    """Special nested class for casting SAESplineJointDutyCycleRating to subclasses."""

    __parent__: "SAESplineJointDutyCycleRating"

    @property
    def sae_spline_joint_duty_cycle_rating(
        self: "CastSelf",
    ) -> "SAESplineJointDutyCycleRating":
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
class SAESplineJointDutyCycleRating(_0.APIBase):
    """SAESplineJointDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SAE_SPLINE_JOINT_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fatigue_damage_for_compressive_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueDamageForCompressiveStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_damage_for_equivalent_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FatigueDamageForEquivalentRootStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_damage_for_tooth_shear_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueDamageForToothShearStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_compressive_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForCompressiveStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_tooth_shear_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForToothShearStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_equivalent_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SafetyFactorForEquivalentRootStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SAESplineJointDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_SAESplineJointDutyCycleRating
        """
        return _Cast_SAESplineJointDutyCycleRating(self)
