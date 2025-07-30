"""DIN5466SplineRating"""

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

_DIN5466_SPLINE_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings", "DIN5466SplineRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors.rating import _1621

    Self = TypeVar("Self", bound="DIN5466SplineRating")
    CastSelf = TypeVar(
        "CastSelf", bound="DIN5466SplineRating._Cast_DIN5466SplineRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DIN5466SplineRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DIN5466SplineRating:
    """Special nested class for casting DIN5466SplineRating to subclasses."""

    __parent__: "DIN5466SplineRating"

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
    def din5466_spline_rating(self: "CastSelf") -> "DIN5466SplineRating":
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
class DIN5466SplineRating(_1617.SplineJointRating):
    """DIN5466SplineRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DIN5466_SPLINE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def resultant_shear_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultantShearForce")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_DIN5466SplineRating":
        """Cast to another type.

        Returns:
            _Cast_DIN5466SplineRating
        """
        return _Cast_DIN5466SplineRating(self)
