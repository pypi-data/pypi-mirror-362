"""SAESplineJointRating"""

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
from mastapy._private.detailed_rigid_connectors.splines.ratings import _1617

_SAE_SPLINE_JOINT_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings", "SAESplineJointRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors.rating import _1621

    Self = TypeVar("Self", bound="SAESplineJointRating")
    CastSelf = TypeVar(
        "CastSelf", bound="SAESplineJointRating._Cast_SAESplineJointRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SAESplineJointRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SAESplineJointRating:
    """Special nested class for casting SAESplineJointRating to subclasses."""

    __parent__: "SAESplineJointRating"

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
    def sae_spline_joint_rating(self: "CastSelf") -> "SAESplineJointRating":
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
class SAESplineJointRating(_1617.SplineJointRating):
    """SAESplineJointRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SAE_SPLINE_JOINT_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_contact_height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveContactHeight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_compressive_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableCompressiveStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_shear_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableShearStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_tensile_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableTensileStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def calculated_compressive_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedCompressiveStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def calculated_maximum_tooth_shearing_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CalculatedMaximumToothShearingStress"
        )

        if temp is None:
            return 0.0

        return temp

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
    def fatigue_damage_for_tooth_shearing_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FatigueDamageForToothShearingStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_life_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueLifeFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def internal_hoop_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InternalHoopStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def misalignment_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentFactor")

        if temp is None:
            return 0.0

        return temp

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
    def over_load_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverLoadFactor")

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
    def wear_life_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WearLifeFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SAESplineJointRating":
        """Cast to another type.

        Returns:
            _Cast_SAESplineJointRating
        """
        return _Cast_SAESplineJointRating(self)
