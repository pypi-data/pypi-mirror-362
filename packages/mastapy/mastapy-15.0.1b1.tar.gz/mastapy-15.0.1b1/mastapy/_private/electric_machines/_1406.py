"""HairpinConductor"""

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
from mastapy._private.electric_machines import _1450

_HAIRPIN_CONDUCTOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "HairpinConductor"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HairpinConductor")
    CastSelf = TypeVar("CastSelf", bound="HairpinConductor._Cast_HairpinConductor")


__docformat__ = "restructuredtext en"
__all__ = ("HairpinConductor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HairpinConductor:
    """Special nested class for casting HairpinConductor to subclasses."""

    __parent__: "HairpinConductor"

    @property
    def winding_conductor(self: "CastSelf") -> "_1450.WindingConductor":
        return self.__parent__._cast(_1450.WindingConductor)

    @property
    def hairpin_conductor(self: "CastSelf") -> "HairpinConductor":
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
class HairpinConductor(_1450.WindingConductor):
    """HairpinConductor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HAIRPIN_CONDUCTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Angle")

        if temp is None:
            return 0.0

        return temp

    @angle.setter
    @exception_bridge
    @enforce_parameter_types
    def angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Angle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def angle_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngleOffset")

        if temp is None:
            return 0.0

        return temp

    @angle_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def angle_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AngleOffset", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def corner_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CornerRadius")

        if temp is None:
            return 0.0

        return temp

    @corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def corner_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CornerRadius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def radial_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialOffset")

        if temp is None:
            return 0.0

        return temp

    @radial_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialOffset", float(value) if value is not None else 0.0
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
    @exception_bridge
    def winding_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindingArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def winding_material_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WindingMaterialHeight")

        if temp is None:
            return 0.0

        return temp

    @winding_material_height.setter
    @exception_bridge
    @enforce_parameter_types
    def winding_material_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WindingMaterialHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def winding_material_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WindingMaterialWidth")

        if temp is None:
            return 0.0

        return temp

    @winding_material_width.setter
    @exception_bridge
    @enforce_parameter_types
    def winding_material_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WindingMaterialWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_HairpinConductor":
        """Cast to another type.

        Returns:
            _Cast_HairpinConductor
        """
        return _Cast_HairpinConductor(self)
