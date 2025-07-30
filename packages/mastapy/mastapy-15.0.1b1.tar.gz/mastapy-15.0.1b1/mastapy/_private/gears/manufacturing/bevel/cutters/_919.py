"""WheelRoughCutter"""

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

_WHEEL_ROUGH_CUTTER = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel.Cutters", "WheelRoughCutter"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WheelRoughCutter")
    CastSelf = TypeVar("CastSelf", bound="WheelRoughCutter._Cast_WheelRoughCutter")


__docformat__ = "restructuredtext en"
__all__ = ("WheelRoughCutter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WheelRoughCutter:
    """Special nested class for casting WheelRoughCutter to subclasses."""

    __parent__: "WheelRoughCutter"

    @property
    def conical_gear_cutter(self: "CastSelf") -> "_1273.ConicalGearCutter":
        return self.__parent__._cast(_1273.ConicalGearCutter)

    @property
    def wheel_rough_cutter(self: "CastSelf") -> "WheelRoughCutter":
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
class WheelRoughCutter(_1273.ConicalGearCutter):
    """WheelRoughCutter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WHEEL_ROUGH_CUTTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def delta_bg(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaBG")

        if temp is None:
            return 0.0

        return temp

    @delta_bg.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_bg(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaBG", float(value) if value is not None else 0.0
        )

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
    def point_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PointWidth")

        if temp is None:
            return 0.0

        return temp

    @point_width.setter
    @exception_bridge
    @enforce_parameter_types
    def point_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PointWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def stock_allowance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StockAllowance")

        if temp is None:
            return 0.0

        return temp

    @stock_allowance.setter
    @exception_bridge
    @enforce_parameter_types
    def stock_allowance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StockAllowance", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_WheelRoughCutter":
        """Cast to another type.

        Returns:
            _Cast_WheelRoughCutter
        """
        return _Cast_WheelRoughCutter(self)
