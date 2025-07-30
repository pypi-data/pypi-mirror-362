"""KeywayRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.detailed_rigid_connectors.interference_fits.rating import _1634

_KEYWAY_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints.Rating", "KeywayRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors.keyed_joints import _1622
    from mastapy._private.detailed_rigid_connectors.keyed_joints.rating import _1626
    from mastapy._private.detailed_rigid_connectors.rating import _1621

    Self = TypeVar("Self", bound="KeywayRating")
    CastSelf = TypeVar("CastSelf", bound="KeywayRating._Cast_KeywayRating")


__docformat__ = "restructuredtext en"
__all__ = ("KeywayRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KeywayRating:
    """Special nested class for casting KeywayRating to subclasses."""

    __parent__: "KeywayRating"

    @property
    def interference_fit_rating(self: "CastSelf") -> "_1634.InterferenceFitRating":
        return self.__parent__._cast(_1634.InterferenceFitRating)

    @property
    def shaft_hub_connection_rating(
        self: "CastSelf",
    ) -> "_1621.ShaftHubConnectionRating":
        from mastapy._private.detailed_rigid_connectors.rating import _1621

        return self.__parent__._cast(_1621.ShaftHubConnectionRating)

    @property
    def keyway_rating(self: "CastSelf") -> "KeywayRating":
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
class KeywayRating(_1634.InterferenceFitRating):
    """KeywayRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KEYWAY_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def application_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ApplicationFactor")

        if temp is None:
            return 0.0

        return temp

    @application_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def application_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ApplicationFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def circumferential_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CircumferentialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def extreme_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExtremeForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def extreme_load_carrying_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExtremeLoadCarryingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def frictional_engagement_factor_extreme_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FrictionalEngagementFactorExtremeLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def frictional_engagement_factor_rated_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FrictionalEngagementFactorRatedLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def frictional_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionalTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inner_component_extreme_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerComponentExtremeSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inner_component_rated_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerComponentRatedSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def key_extreme_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KeyExtremeSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def key_rated_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KeyRatedSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_distribution_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_distribution_factor_single_key(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactorSingleKey")

        if temp is None:
            return 0.0

        return temp

    @load_distribution_factor_single_key.setter
    @exception_bridge
    @enforce_parameter_types
    def load_distribution_factor_single_key(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LoadDistributionFactorSingleKey",
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
    def number_of_torque_peaks(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTorquePeaks")

        if temp is None:
            return 0.0

        return temp

    @number_of_torque_peaks.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_torque_peaks(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTorquePeaks",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_torque_reversals(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTorqueReversals")

        if temp is None:
            return 0.0

        return temp

    @number_of_torque_reversals.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_torque_reversals(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTorqueReversals",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def outer_component_extreme_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterComponentExtremeSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_component_rated_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterComponentRatedSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rated_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatedForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rated_load_carrying_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatedLoadCarryingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_peak_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorquePeakFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_reversal_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueReversalFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def keyed_joint_design(self: "Self") -> "_1622.KeyedJointDesign":
        """mastapy.detailed_rigid_connectors.keyed_joints.KeyedJointDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KeyedJointDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def keyway_half_ratings(self: "Self") -> "List[_1626.KeywayHalfRating]":
        """List[mastapy.detailed_rigid_connectors.keyed_joints.rating.KeywayHalfRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KeywayHalfRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_KeywayRating":
        """Cast to another type.

        Returns:
            _Cast_KeywayRating
        """
        return _Cast_KeywayRating(self)
