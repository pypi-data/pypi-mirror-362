"""ExcelSheetDesignStateSelector"""

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
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_EXCEL_SHEET_DESIGN_STATE_SELECTOR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DutyCycles.ExcelBatchDutyCycles",
    "ExcelSheetDesignStateSelector",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ExcelSheetDesignStateSelector")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ExcelSheetDesignStateSelector._Cast_ExcelSheetDesignStateSelector",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExcelSheetDesignStateSelector",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExcelSheetDesignStateSelector:
    """Special nested class for casting ExcelSheetDesignStateSelector to subclasses."""

    __parent__: "ExcelSheetDesignStateSelector"

    @property
    def excel_sheet_design_state_selector(
        self: "CastSelf",
    ) -> "ExcelSheetDesignStateSelector":
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
class ExcelSheetDesignStateSelector(_0.APIBase):
    """ExcelSheetDesignStateSelector

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXCEL_SHEET_DESIGN_STATE_SELECTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def design_state(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "DesignState")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @design_state.setter
    @exception_bridge
    @enforce_parameter_types
    def design_state(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DesignState", value)

    @property
    @exception_bridge
    def sheet_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SheetName")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ExcelSheetDesignStateSelector":
        """Cast to another type.

        Returns:
            _Cast_ExcelSheetDesignStateSelector
        """
        return _Cast_ExcelSheetDesignStateSelector(self)
