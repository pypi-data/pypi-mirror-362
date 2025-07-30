"""SpecifiedConcentricPartGroupDrawingOrder"""

from __future__ import annotations

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
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.part_groups import _2722

_SPECIFIED_CONCENTRIC_PART_GROUP_DRAWING_ORDER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Projections",
    "SpecifiedConcentricPartGroupDrawingOrder",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SpecifiedConcentricPartGroupDrawingOrder")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecifiedConcentricPartGroupDrawingOrder._Cast_SpecifiedConcentricPartGroupDrawingOrder",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecifiedConcentricPartGroupDrawingOrder",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecifiedConcentricPartGroupDrawingOrder:
    """Special nested class for casting SpecifiedConcentricPartGroupDrawingOrder to subclasses."""

    __parent__: "SpecifiedConcentricPartGroupDrawingOrder"

    @property
    def specified_concentric_part_group_drawing_order(
        self: "CastSelf",
    ) -> "SpecifiedConcentricPartGroupDrawingOrder":
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
class SpecifiedConcentricPartGroupDrawingOrder(_0.APIBase):
    """SpecifiedConcentricPartGroupDrawingOrder

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIFIED_CONCENTRIC_PART_GROUP_DRAWING_ORDER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def concentric_group(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup":
        """ListWithSelectedItem[mastapy.system_model.part_model.part_groups.ConcentricPartGroup]"""
        temp = pythonnet_property_get(self.wrapped, "ConcentricGroup")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_ConcentricPartGroup",
        )(temp)

    @concentric_group.setter
    @exception_bridge
    @enforce_parameter_types
    def concentric_group(self: "Self", value: "_2722.ConcentricPartGroup") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ConcentricGroup", value)

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @exception_bridge
    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @property
    def cast_to(self: "Self") -> "_Cast_SpecifiedConcentricPartGroupDrawingOrder":
        """Cast to another type.

        Returns:
            _Cast_SpecifiedConcentricPartGroupDrawingOrder
        """
        return _Cast_SpecifiedConcentricPartGroupDrawingOrder(self)
