"""AGMA6123SplineHalfRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.detailed_rigid_connectors.splines.ratings import _1616

_AGMA6123_SPLINE_HALF_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings", "AGMA6123SplineHalfRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AGMA6123SplineHalfRating")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMA6123SplineHalfRating._Cast_AGMA6123SplineHalfRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMA6123SplineHalfRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMA6123SplineHalfRating:
    """Special nested class for casting AGMA6123SplineHalfRating to subclasses."""

    __parent__: "AGMA6123SplineHalfRating"

    @property
    def spline_half_rating(self: "CastSelf") -> "_1616.SplineHalfRating":
        return self.__parent__._cast(_1616.SplineHalfRating)

    @property
    def agma6123_spline_half_rating(self: "CastSelf") -> "AGMA6123SplineHalfRating":
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
class AGMA6123SplineHalfRating(_1616.SplineHalfRating):
    """AGMA6123SplineHalfRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA6123_SPLINE_HALF_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_stress_for_bursting(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableStressForBursting")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_stress_for_shearing(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableStressForShearing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_torque_for_shearing(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableTorqueForShearing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_torque_for_wear_and_fretting(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableTorqueForWearAndFretting")

        if temp is None:
            return 0.0

        return temp

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
    def cast_to(self: "Self") -> "_Cast_AGMA6123SplineHalfRating":
        """Cast to another type.

        Returns:
            _Cast_AGMA6123SplineHalfRating
        """
        return _Cast_AGMA6123SplineHalfRating(self)
