"""SplineHalfRating"""

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

_SPLINE_HALF_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings", "SplineHalfRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors.splines.ratings import (
        _1608,
        _1610,
        _1612,
        _1614,
    )

    Self = TypeVar("Self", bound="SplineHalfRating")
    CastSelf = TypeVar("CastSelf", bound="SplineHalfRating._Cast_SplineHalfRating")


__docformat__ = "restructuredtext en"
__all__ = ("SplineHalfRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SplineHalfRating:
    """Special nested class for casting SplineHalfRating to subclasses."""

    __parent__: "SplineHalfRating"

    @property
    def agma6123_spline_half_rating(
        self: "CastSelf",
    ) -> "_1608.AGMA6123SplineHalfRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1608

        return self.__parent__._cast(_1608.AGMA6123SplineHalfRating)

    @property
    def din5466_spline_half_rating(self: "CastSelf") -> "_1610.DIN5466SplineHalfRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1610

        return self.__parent__._cast(_1610.DIN5466SplineHalfRating)

    @property
    def gbt17855_spline_half_rating(
        self: "CastSelf",
    ) -> "_1612.GBT17855SplineHalfRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1612

        return self.__parent__._cast(_1612.GBT17855SplineHalfRating)

    @property
    def sae_spline_half_rating(self: "CastSelf") -> "_1614.SAESplineHalfRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1614

        return self.__parent__._cast(_1614.SAESplineHalfRating)

    @property
    def spline_half_rating(self: "CastSelf") -> "SplineHalfRating":
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
class SplineHalfRating(_0.APIBase):
    """SplineHalfRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPLINE_HALF_RATING

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
    def cast_to(self: "Self") -> "_Cast_SplineHalfRating":
        """Cast to another type.

        Returns:
            _Cast_SplineHalfRating
        """
        return _Cast_SplineHalfRating(self)
