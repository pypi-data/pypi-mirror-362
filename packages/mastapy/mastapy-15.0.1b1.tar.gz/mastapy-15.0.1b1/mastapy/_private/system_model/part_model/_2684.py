"""GuideModelUsage"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GUIDE_MODEL_USAGE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "GuideModelUsage"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GuideModelUsage")
    CastSelf = TypeVar("CastSelf", bound="GuideModelUsage._Cast_GuideModelUsage")


__docformat__ = "restructuredtext en"
__all__ = ("GuideModelUsage",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GuideModelUsage:
    """Special nested class for casting GuideModelUsage to subclasses."""

    __parent__: "GuideModelUsage"

    @property
    def guide_model_usage(self: "CastSelf") -> "GuideModelUsage":
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
class GuideModelUsage(_0.APIBase):
    """GuideModelUsage

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GUIDE_MODEL_USAGE

    class AlignmentOptions(Enum):
        """AlignmentOptions is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _GUIDE_MODEL_USAGE.AlignmentOptions

        LEFT_EDGE_TO_LEFT_OFFSET_OF_SHAFT = 0
        LEFT_EDGE_TO_ZERO_OFFSET_OF_SHAFT = 1

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    AlignmentOptions.__setattr__ = __enum_setattr
    AlignmentOptions.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def alignment_method(self: "Self") -> "GuideModelUsage.AlignmentOptions":
        """mastapy.system_model.part_model.GuideModelUsage.AlignmentOptions"""
        temp = pythonnet_property_get(self.wrapped, "AlignmentMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PartModel.GuideModelUsage+AlignmentOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model.GuideModelUsage.GuideModelUsage",
            "AlignmentOptions",
        )(value)

    @alignment_method.setter
    @exception_bridge
    @enforce_parameter_types
    def alignment_method(
        self: "Self", value: "GuideModelUsage.AlignmentOptions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PartModel.GuideModelUsage+AlignmentOptions"
        )
        pythonnet_property_set(self.wrapped, "AlignmentMethod", value)

    @property
    @exception_bridge
    def clip_drawing(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ClipDrawing")

        if temp is None:
            return False

        return temp

    @clip_drawing.setter
    @exception_bridge
    @enforce_parameter_types
    def clip_drawing(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ClipDrawing", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def clipping_bottom(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ClippingBottom")

        if temp is None:
            return 0.0

        return temp

    @clipping_bottom.setter
    @exception_bridge
    @enforce_parameter_types
    def clipping_bottom(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ClippingBottom", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def clipping_left(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ClippingLeft")

        if temp is None:
            return 0.0

        return temp

    @clipping_left.setter
    @exception_bridge
    @enforce_parameter_types
    def clipping_left(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ClippingLeft", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def clipping_right(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ClippingRight")

        if temp is None:
            return 0.0

        return temp

    @clipping_right.setter
    @exception_bridge
    @enforce_parameter_types
    def clipping_right(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ClippingRight", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def clipping_top(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ClippingTop")

        if temp is None:
            return 0.0

        return temp

    @clipping_top.setter
    @exception_bridge
    @enforce_parameter_types
    def clipping_top(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ClippingTop", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def force_monochrome(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ForceMonochrome")

        if temp is None:
            return False

        return temp

    @force_monochrome.setter
    @exception_bridge
    @enforce_parameter_types
    def force_monochrome(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ForceMonochrome", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def layout(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "Layout")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @layout.setter
    @exception_bridge
    @enforce_parameter_types
    def layout(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Layout", value)

    @property
    @exception_bridge
    def origin_horizontal(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OriginHorizontal")

        if temp is None:
            return 0.0

        return temp

    @origin_horizontal.setter
    @exception_bridge
    @enforce_parameter_types
    def origin_horizontal(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OriginHorizontal", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def origin_vertical(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OriginVertical")

        if temp is None:
            return 0.0

        return temp

    @origin_vertical.setter
    @exception_bridge
    @enforce_parameter_types
    def origin_vertical(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OriginVertical", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def rotation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Rotation")

        if temp is None:
            return 0.0

        return temp

    @rotation.setter
    @exception_bridge
    @enforce_parameter_types
    def rotation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Rotation", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GuideModelUsage":
        """Cast to another type.

        Returns:
            _Cast_GuideModelUsage
        """
        return _Cast_GuideModelUsage(self)
