"""PointsForSurface"""

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
from mastapy._private._math.vector_3d import Vector3D

_POINTS_FOR_SURFACE = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Charts", "PointsForSurface"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="PointsForSurface")
    CastSelf = TypeVar("CastSelf", bound="PointsForSurface._Cast_PointsForSurface")


__docformat__ = "restructuredtext en"
__all__ = ("PointsForSurface",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PointsForSurface:
    """Special nested class for casting PointsForSurface to subclasses."""

    __parent__: "PointsForSurface"

    @property
    def points_for_surface(self: "CastSelf") -> "PointsForSurface":
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
class PointsForSurface(_0.APIBase):
    """PointsForSurface

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POINTS_FOR_SURFACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def points(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Points")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_PointsForSurface":
        """Cast to another type.

        Returns:
            _Cast_PointsForSurface
        """
        return _Cast_PointsForSurface(self)
