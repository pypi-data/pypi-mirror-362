"""MagnetForLayer"""

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
from mastapy._private.electric_machines import _1415

_MAGNET_FOR_LAYER = python_net_import("SMT.MastaAPI.ElectricMachines", "MagnetForLayer")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MagnetForLayer")
    CastSelf = TypeVar("CastSelf", bound="MagnetForLayer._Cast_MagnetForLayer")


__docformat__ = "restructuredtext en"
__all__ = ("MagnetForLayer",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MagnetForLayer:
    """Special nested class for casting MagnetForLayer to subclasses."""

    __parent__: "MagnetForLayer"

    @property
    def magnet_design(self: "CastSelf") -> "_1415.MagnetDesign":
        return self.__parent__._cast(_1415.MagnetDesign)

    @property
    def magnet_for_layer(self: "CastSelf") -> "MagnetForLayer":
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
class MagnetForLayer(_1415.MagnetDesign):
    """MagnetForLayer

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MAGNET_FOR_LAYER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_segments_along_width(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfSegmentsAlongWidth")

        if temp is None:
            return 0

        return temp

    @number_of_segments_along_width.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_segments_along_width(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfSegmentsAlongWidth",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Thickness")

        if temp is None:
            return 0.0

        return temp

    @thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Thickness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def width_of_each_segment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WidthOfEachSegment")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_MagnetForLayer":
        """Cast to another type.

        Returns:
            _Cast_MagnetForLayer
        """
        return _Cast_MagnetForLayer(self)
