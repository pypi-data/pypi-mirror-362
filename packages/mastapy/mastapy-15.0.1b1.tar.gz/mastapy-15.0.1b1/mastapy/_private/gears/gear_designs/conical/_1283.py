"""DummyConicalGearCutter"""

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

_DUMMY_CONICAL_GEAR_CUTTER = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "DummyConicalGearCutter"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DummyConicalGearCutter")
    CastSelf = TypeVar(
        "CastSelf", bound="DummyConicalGearCutter._Cast_DummyConicalGearCutter"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DummyConicalGearCutter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DummyConicalGearCutter:
    """Special nested class for casting DummyConicalGearCutter to subclasses."""

    __parent__: "DummyConicalGearCutter"

    @property
    def conical_gear_cutter(self: "CastSelf") -> "_1273.ConicalGearCutter":
        return self.__parent__._cast(_1273.ConicalGearCutter)

    @property
    def dummy_conical_gear_cutter(self: "CastSelf") -> "DummyConicalGearCutter":
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
class DummyConicalGearCutter(_1273.ConicalGearCutter):
    """DummyConicalGearCutter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DUMMY_CONICAL_GEAR_CUTTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def finish_cutter_point_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FinishCutterPointWidth")

        if temp is None:
            return 0.0

        return temp

    @finish_cutter_point_width.setter
    @exception_bridge
    @enforce_parameter_types
    def finish_cutter_point_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FinishCutterPointWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def inner_edge_radius_convex(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerEdgeRadiusConvex")

        if temp is None:
            return 0.0

        return temp

    @inner_edge_radius_convex.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_edge_radius_convex(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerEdgeRadiusConvex",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_blade_groups(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfBladeGroups")

        if temp is None:
            return 0

        return temp

    @number_of_blade_groups.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_blade_groups(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfBladeGroups", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def outer_edge_radius_concave(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterEdgeRadiusConcave")

        if temp is None:
            return 0.0

        return temp

    @outer_edge_radius_concave.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_edge_radius_concave(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterEdgeRadiusConcave",
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
    def cast_to(self: "Self") -> "_Cast_DummyConicalGearCutter":
        """Cast to another type.

        Returns:
            _Cast_DummyConicalGearCutter
        """
        return _Cast_DummyConicalGearCutter(self)
