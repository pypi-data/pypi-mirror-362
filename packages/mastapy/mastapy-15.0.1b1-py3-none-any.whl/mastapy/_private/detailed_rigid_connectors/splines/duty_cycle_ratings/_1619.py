"""GBT17855SplineJointDutyCycleRating"""

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

_GBT17855_SPLINE_JOINT_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.DutyCycleRatings",
    "GBT17855SplineJointDutyCycleRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GBT17855SplineJointDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GBT17855SplineJointDutyCycleRating._Cast_GBT17855SplineJointDutyCycleRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GBT17855SplineJointDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GBT17855SplineJointDutyCycleRating:
    """Special nested class for casting GBT17855SplineJointDutyCycleRating to subclasses."""

    __parent__: "GBT17855SplineJointDutyCycleRating"

    @property
    def gbt17855_spline_joint_duty_cycle_rating(
        self: "CastSelf",
    ) -> "GBT17855SplineJointDutyCycleRating":
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
class GBT17855SplineJointDutyCycleRating(_0.APIBase):
    """GBT17855SplineJointDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GBT17855_SPLINE_JOINT_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def safety_factor_for_equivalent_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForEquivalentStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_root_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForRootBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_tooth_shearing_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SafetyFactorForToothShearingStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_wearing_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForWearingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GBT17855SplineJointDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_GBT17855SplineJointDutyCycleRating
        """
        return _Cast_GBT17855SplineJointDutyCycleRating(self)
