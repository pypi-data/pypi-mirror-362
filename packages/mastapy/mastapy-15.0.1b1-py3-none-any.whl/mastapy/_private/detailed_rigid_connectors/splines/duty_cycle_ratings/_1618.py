"""AGMA6123SplineJointDutyCycleRating"""

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

_AGMA6123_SPLINE_JOINT_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.DutyCycleRatings",
    "AGMA6123SplineJointDutyCycleRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AGMA6123SplineJointDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMA6123SplineJointDutyCycleRating._Cast_AGMA6123SplineJointDutyCycleRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMA6123SplineJointDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMA6123SplineJointDutyCycleRating:
    """Special nested class for casting AGMA6123SplineJointDutyCycleRating to subclasses."""

    __parent__: "AGMA6123SplineJointDutyCycleRating"

    @property
    def agma6123_spline_joint_duty_cycle_rating(
        self: "CastSelf",
    ) -> "AGMA6123SplineJointDutyCycleRating":
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
class AGMA6123SplineJointDutyCycleRating(_0.APIBase):
    """AGMA6123SplineJointDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA6123_SPLINE_JOINT_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def safety_factor_for_ring_bursting(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForRingBursting")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_shearing(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForShearing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_torsional_failure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForTorsionalFailure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_wear_and_fretting(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForWearAndFretting")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AGMA6123SplineJointDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_AGMA6123SplineJointDutyCycleRating
        """
        return _Cast_AGMA6123SplineJointDutyCycleRating(self)
