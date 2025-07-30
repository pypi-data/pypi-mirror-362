"""DIN5466SplineHalfRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.detailed_rigid_connectors.splines.ratings import _1616

_DIN5466_SPLINE_HALF_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings", "DIN5466SplineHalfRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DIN5466SplineHalfRating")
    CastSelf = TypeVar(
        "CastSelf", bound="DIN5466SplineHalfRating._Cast_DIN5466SplineHalfRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DIN5466SplineHalfRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DIN5466SplineHalfRating:
    """Special nested class for casting DIN5466SplineHalfRating to subclasses."""

    __parent__: "DIN5466SplineHalfRating"

    @property
    def spline_half_rating(self: "CastSelf") -> "_1616.SplineHalfRating":
        return self.__parent__._cast(_1616.SplineHalfRating)

    @property
    def din5466_spline_half_rating(self: "CastSelf") -> "DIN5466SplineHalfRating":
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
class DIN5466SplineHalfRating(_1616.SplineHalfRating):
    """DIN5466SplineHalfRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DIN5466_SPLINE_HALF_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DIN5466SplineHalfRating":
        """Cast to another type.

        Returns:
            _Cast_DIN5466SplineHalfRating
        """
        return _Cast_DIN5466SplineHalfRating(self)
