"""GearNURBSSurface"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears import _409

_GEAR_NURBS_SURFACE = python_net_import("SMT.MastaAPI.Gears", "GearNURBSSurface")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearNURBSSurface")
    CastSelf = TypeVar("CastSelf", bound="GearNURBSSurface._Cast_GearNURBSSurface")


__docformat__ = "restructuredtext en"
__all__ = ("GearNURBSSurface",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearNURBSSurface:
    """Special nested class for casting GearNURBSSurface to subclasses."""

    __parent__: "GearNURBSSurface"

    @property
    def conical_gear_tooth_surface(self: "CastSelf") -> "_409.ConicalGearToothSurface":
        return self.__parent__._cast(_409.ConicalGearToothSurface)

    @property
    def gear_nurbs_surface(self: "CastSelf") -> "GearNURBSSurface":
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
class GearNURBSSurface(_409.ConicalGearToothSurface):
    """GearNURBSSurface

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_NURBS_SURFACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearNURBSSurface":
        """Cast to another type.

        Returns:
            _Cast_GearNURBSSurface
        """
        return _Cast_GearNURBSSurface(self)
