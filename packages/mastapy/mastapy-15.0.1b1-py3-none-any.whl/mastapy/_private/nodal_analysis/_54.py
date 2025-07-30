"""BarGeometry"""

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

_BAR_GEOMETRY = python_net_import("SMT.MastaAPI.NodalAnalysis", "BarGeometry")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BarGeometry")
    CastSelf = TypeVar("CastSelf", bound="BarGeometry._Cast_BarGeometry")


__docformat__ = "restructuredtext en"
__all__ = ("BarGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BarGeometry:
    """Special nested class for casting BarGeometry to subclasses."""

    __parent__: "BarGeometry"

    @property
    def bar_geometry(self: "CastSelf") -> "BarGeometry":
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
class BarGeometry(_0.APIBase):
    """BarGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BAR_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cross_sectional_area_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CrossSectionalAreaRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def polar_area_moment_of_inertia_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PolarAreaMomentOfInertiaRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_BarGeometry":
        """Cast to another type.

        Returns:
            _Cast_BarGeometry
        """
        return _Cast_BarGeometry(self)
