"""ClampedSection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_CLAMPED_SECTION = python_net_import("SMT.MastaAPI.Bolts", "ClampedSection")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bolts import _1651

    Self = TypeVar("Self", bound="ClampedSection")
    CastSelf = TypeVar("CastSelf", bound="ClampedSection._Cast_ClampedSection")


__docformat__ = "restructuredtext en"
__all__ = ("ClampedSection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ClampedSection:
    """Special nested class for casting ClampedSection to subclasses."""

    __parent__: "ClampedSection"

    @property
    def clamped_section(self: "CastSelf") -> "ClampedSection":
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
class ClampedSection(_0.APIBase):
    """ClampedSection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CLAMPED_SECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def edit_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "EditMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @edit_material.setter
    @exception_bridge
    @enforce_parameter_types
    def edit_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "EditMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def part_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PartThickness")

        if temp is None:
            return 0.0

        return temp

    @part_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def part_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PartThickness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def material(self: "Self") -> "_1651.BoltedJointMaterial":
        """mastapy.bolts.BoltedJointMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Material")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ClampedSection":
        """Cast to another type.

        Returns:
            _Cast_ClampedSection
        """
        return _Cast_ClampedSection(self)
