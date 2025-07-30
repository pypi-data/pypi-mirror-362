"""FieldWindingSpecification"""

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
from mastapy._private.electric_machines import _1399

_FIELD_WINDING_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "FieldWindingSpecification"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FieldWindingSpecification")
    CastSelf = TypeVar(
        "CastSelf", bound="FieldWindingSpecification._Cast_FieldWindingSpecification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FieldWindingSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FieldWindingSpecification:
    """Special nested class for casting FieldWindingSpecification to subclasses."""

    __parent__: "FieldWindingSpecification"

    @property
    def field_winding_specification_base(
        self: "CastSelf",
    ) -> "_1399.FieldWindingSpecificationBase":
        return self.__parent__._cast(_1399.FieldWindingSpecificationBase)

    @property
    def field_winding_specification(self: "CastSelf") -> "FieldWindingSpecification":
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
class FieldWindingSpecification(_1399.FieldWindingSpecificationBase):
    """FieldWindingSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FIELD_WINDING_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def coil_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CoilHeight")

        if temp is None:
            return 0.0

        return temp

    @coil_height.setter
    @exception_bridge
    @enforce_parameter_types
    def coil_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CoilHeight", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def coil_radial_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CoilRadialOffset")

        if temp is None:
            return 0.0

        return temp

    @coil_radial_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def coil_radial_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CoilRadialOffset", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def coil_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CoilWidth")

        if temp is None:
            return 0.0

        return temp

    @coil_width.setter
    @exception_bridge
    @enforce_parameter_types
    def coil_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CoilWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def field_winding_edge_is_radial_line(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "FieldWindingEdgeIsRadialLine")

        if temp is None:
            return False

        return temp

    @field_winding_edge_is_radial_line.setter
    @exception_bridge
    @enforce_parameter_types
    def field_winding_edge_is_radial_line(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FieldWindingEdgeIsRadialLine",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FieldWindingSpecification":
        """Cast to another type.

        Returns:
            _Cast_FieldWindingSpecification
        """
        return _Cast_FieldWindingSpecification(self)
