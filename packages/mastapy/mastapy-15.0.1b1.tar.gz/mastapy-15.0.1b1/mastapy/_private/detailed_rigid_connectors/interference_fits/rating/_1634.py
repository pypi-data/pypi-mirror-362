"""InterferenceFitRating"""

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
from mastapy._private.detailed_rigid_connectors.rating import _1621

_INTERFERENCE_FIT_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits.Rating",
    "InterferenceFitRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors.keyed_joints.rating import _1627

    Self = TypeVar("Self", bound="InterferenceFitRating")
    CastSelf = TypeVar(
        "CastSelf", bound="InterferenceFitRating._Cast_InterferenceFitRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterferenceFitRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterferenceFitRating:
    """Special nested class for casting InterferenceFitRating to subclasses."""

    __parent__: "InterferenceFitRating"

    @property
    def shaft_hub_connection_rating(
        self: "CastSelf",
    ) -> "_1621.ShaftHubConnectionRating":
        return self.__parent__._cast(_1621.ShaftHubConnectionRating)

    @property
    def keyway_rating(self: "CastSelf") -> "_1627.KeywayRating":
        from mastapy._private.detailed_rigid_connectors.keyed_joints.rating import _1627

        return self.__parent__._cast(_1627.KeywayRating)

    @property
    def interference_fit_rating(self: "CastSelf") -> "InterferenceFitRating":
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
class InterferenceFitRating(_1621.ShaftHubConnectionRating):
    """InterferenceFitRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTERFERENCE_FIT_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_axial_force_stationary(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableAxialForceStationary")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_axial_force_at_operating_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllowableAxialForceAtOperatingSpeed"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_torque_stationary(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableTorqueStationary")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_torque_at_operating_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableTorqueAtOperatingSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def diameter_of_joint(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiameterOfJoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def joint_pressure_at_operating_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "JointPressureAtOperatingSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_joint(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthOfJoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peripheral_speed_of_outer_part(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeripheralSpeedOfOuterPart")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peripheral_speed_of_outer_part_causing_loss_of_interference(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PeripheralSpeedOfOuterPartCausingLossOfInterference"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_axial_force_stationary(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleAxialForceStationary")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_axial_force_at_operating_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialForceAtOperatingSpeed"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_torque_stationary(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleTorqueStationary")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_torque_at_operating_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleTorqueAtOperatingSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def required_fit_for_avoidance_of_fretting_wear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RequiredFitForAvoidanceOfFrettingWear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForAxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_axial_force_stationary(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SafetyFactorForAxialForceStationary"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_torque_stationary(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForTorqueStationary")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_InterferenceFitRating":
        """Cast to another type.

        Returns:
            _Cast_InterferenceFitRating
        """
        return _Cast_InterferenceFitRating(self)
