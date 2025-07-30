"""KeywayHalfRating"""

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

_KEYWAY_HALF_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints.Rating", "KeywayHalfRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="KeywayHalfRating")
    CastSelf = TypeVar("CastSelf", bound="KeywayHalfRating._Cast_KeywayHalfRating")


__docformat__ = "restructuredtext en"
__all__ = ("KeywayHalfRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KeywayHalfRating:
    """Special nested class for casting KeywayHalfRating to subclasses."""

    __parent__: "KeywayHalfRating"

    @property
    def keyway_half_rating(self: "CastSelf") -> "KeywayHalfRating":
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
class KeywayHalfRating(_0.APIBase):
    """KeywayHalfRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KEYWAY_HALF_RATING

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
    def cast_to(self: "Self") -> "_Cast_KeywayHalfRating":
        """Cast to another type.

        Returns:
            _Cast_KeywayHalfRating
        """
        return _Cast_KeywayHalfRating(self)
