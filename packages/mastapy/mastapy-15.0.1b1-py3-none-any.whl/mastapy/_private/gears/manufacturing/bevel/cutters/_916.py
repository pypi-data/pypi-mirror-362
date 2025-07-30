"""PinionFinishCutter"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.conical import _1273

_PINION_FINISH_CUTTER = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel.Cutters", "PinionFinishCutter"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PinionFinishCutter")
    CastSelf = TypeVar("CastSelf", bound="PinionFinishCutter._Cast_PinionFinishCutter")


__docformat__ = "restructuredtext en"
__all__ = ("PinionFinishCutter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PinionFinishCutter:
    """Special nested class for casting PinionFinishCutter to subclasses."""

    __parent__: "PinionFinishCutter"

    @property
    def conical_gear_cutter(self: "CastSelf") -> "_1273.ConicalGearCutter":
        return self.__parent__._cast(_1273.ConicalGearCutter)

    @property
    def pinion_finish_cutter(self: "CastSelf") -> "PinionFinishCutter":
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
class PinionFinishCutter(_1273.ConicalGearCutter):
    """PinionFinishCutter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PINION_FINISH_CUTTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def inner_blade_point_radius_convex(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerBladePointRadiusConvex")

        if temp is None:
            return 0.0

        return temp

    @inner_blade_point_radius_convex.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_blade_point_radius_convex(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerBladePointRadiusConvex",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def outer_blade_point_radius_concave(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterBladePointRadiusConcave")

        if temp is None:
            return 0.0

        return temp

    @outer_blade_point_radius_concave.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_blade_point_radius_concave(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterBladePointRadiusConcave",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Radius")

        if temp is None:
            return 0.0

        return temp

    @radius.setter
    @exception_bridge
    @enforce_parameter_types
    def radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Radius", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PinionFinishCutter":
        """Cast to another type.

        Returns:
            _Cast_PinionFinishCutter
        """
        return _Cast_PinionFinishCutter(self)
