"""SplineJointRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.detailed_rigid_connectors.rating import _1621

_SPLINE_JOINT_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings", "SplineJointRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors.splines.ratings import (
        _1609,
        _1611,
        _1613,
        _1615,
        _1616,
    )

    Self = TypeVar("Self", bound="SplineJointRating")
    CastSelf = TypeVar("CastSelf", bound="SplineJointRating._Cast_SplineJointRating")


__docformat__ = "restructuredtext en"
__all__ = ("SplineJointRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SplineJointRating:
    """Special nested class for casting SplineJointRating to subclasses."""

    __parent__: "SplineJointRating"

    @property
    def shaft_hub_connection_rating(
        self: "CastSelf",
    ) -> "_1621.ShaftHubConnectionRating":
        return self.__parent__._cast(_1621.ShaftHubConnectionRating)

    @property
    def agma6123_spline_joint_rating(
        self: "CastSelf",
    ) -> "_1609.AGMA6123SplineJointRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1609

        return self.__parent__._cast(_1609.AGMA6123SplineJointRating)

    @property
    def din5466_spline_rating(self: "CastSelf") -> "_1611.DIN5466SplineRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1611

        return self.__parent__._cast(_1611.DIN5466SplineRating)

    @property
    def gbt17855_spline_joint_rating(
        self: "CastSelf",
    ) -> "_1613.GBT17855SplineJointRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1613

        return self.__parent__._cast(_1613.GBT17855SplineJointRating)

    @property
    def sae_spline_joint_rating(self: "CastSelf") -> "_1615.SAESplineJointRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1615

        return self.__parent__._cast(_1615.SAESplineJointRating)

    @property
    def spline_joint_rating(self: "CastSelf") -> "SplineJointRating":
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
class SplineJointRating(_1621.ShaftHubConnectionRating):
    """SplineJointRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPLINE_JOINT_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_bursting_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableBurstingStress")

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
    def dudley_maximum_effective_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DudleyMaximumEffectiveLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Load")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_cycles(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCycles")

        if temp is None:
            return 0.0

        return temp

    @number_of_cycles.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_cycles(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfCycles", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def spline_half_ratings(self: "Self") -> "List[_1616.SplineHalfRating]":
        """List[mastapy.detailed_rigid_connectors.splines.ratings.SplineHalfRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SplineHalfRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SplineJointRating":
        """Cast to another type.

        Returns:
            _Cast_SplineJointRating
        """
        return _Cast_SplineJointRating(self)
