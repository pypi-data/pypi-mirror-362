"""Series2D"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_2d import Vector2D

_SERIES_2D = python_net_import("SMT.MastaAPI.UtilityGUI.Charts", "Series2D")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="Series2D")
    CastSelf = TypeVar("CastSelf", bound="Series2D._Cast_Series2D")


__docformat__ = "restructuredtext en"
__all__ = ("Series2D",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Series2D:
    """Special nested class for casting Series2D to subclasses."""

    __parent__: "Series2D"

    @property
    def series_2d(self: "CastSelf") -> "Series2D":
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
class Series2D(_0.APIBase):
    """Series2D

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SERIES_2D

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
    def points(self: "Self") -> "List[Vector2D]":
        """List[Vector2D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Points")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector2D)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_Series2D":
        """Cast to another type.

        Returns:
            _Cast_Series2D
        """
        return _Cast_Series2D(self)
