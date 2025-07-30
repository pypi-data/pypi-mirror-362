"""AGMA6123SplineJointRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.detailed_rigid_connectors.splines.ratings import _1617

_AGMA6123_SPLINE_JOINT_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings", "AGMA6123SplineJointRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors.rating import _1621

    Self = TypeVar("Self", bound="AGMA6123SplineJointRating")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMA6123SplineJointRating._Cast_AGMA6123SplineJointRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMA6123SplineJointRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMA6123SplineJointRating:
    """Special nested class for casting AGMA6123SplineJointRating to subclasses."""

    __parent__: "AGMA6123SplineJointRating"

    @property
    def spline_joint_rating(self: "CastSelf") -> "_1617.SplineJointRating":
        return self.__parent__._cast(_1617.SplineJointRating)

    @property
    def shaft_hub_connection_rating(
        self: "CastSelf",
    ) -> "_1621.ShaftHubConnectionRating":
        from mastapy._private.detailed_rigid_connectors.rating import _1621

        return self.__parent__._cast(_1621.ShaftHubConnectionRating)

    @property
    def agma6123_spline_joint_rating(self: "CastSelf") -> "AGMA6123SplineJointRating":
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
class AGMA6123SplineJointRating(_1617.SplineJointRating):
    """AGMA6123SplineJointRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA6123_SPLINE_JOINT_RATING

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
    def allowable_ring_bursting_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableRingBurstingStress")

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
    def allowable_torque_for_torsional_failure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllowableTorqueForTorsionalFailure"
        )

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
    def bursting_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BurstingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def centrifugal_hoop_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CentrifugalHoopStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def diameter_at_half_the_working_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiameterAtHalfTheWorkingDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_distribution_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactor")

        if temp is None:
            return 0.0

        return temp

    @load_distribution_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def load_distribution_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LoadDistributionFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

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
    @exception_bridge
    def tensile_tooth_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TensileToothBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_tensile_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalTensileStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AGMA6123SplineJointRating":
        """Cast to another type.

        Returns:
            _Cast_AGMA6123SplineJointRating
        """
        return _Cast_AGMA6123SplineJointRating(self)
