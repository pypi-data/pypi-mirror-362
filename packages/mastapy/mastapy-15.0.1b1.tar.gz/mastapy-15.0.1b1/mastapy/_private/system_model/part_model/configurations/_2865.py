"""PartDetailSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

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

_PART_DETAIL_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Configurations", "PartDetailSelection"
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.part_model import _2698
    from mastapy._private.system_model.part_model.configurations import (
        _2857,
        _2859,
        _2862,
    )
    from mastapy._private.system_model.part_model.gears import _2747, _2748

    Self = TypeVar("Self", bound="PartDetailSelection")
    CastSelf = TypeVar(
        "CastSelf", bound="PartDetailSelection._Cast_PartDetailSelection"
    )

TPart = TypeVar("TPart", bound="_2698.Part")
TSelectableItem = TypeVar("TSelectableItem")

__docformat__ = "restructuredtext en"
__all__ = ("PartDetailSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartDetailSelection:
    """Special nested class for casting PartDetailSelection to subclasses."""

    __parent__: "PartDetailSelection"

    @property
    def active_cylindrical_gear_set_design_selection(
        self: "CastSelf",
    ) -> "_2747.ActiveCylindricalGearSetDesignSelection":
        from mastapy._private.system_model.part_model.gears import _2747

        return self.__parent__._cast(_2747.ActiveCylindricalGearSetDesignSelection)

    @property
    def active_gear_set_design_selection(
        self: "CastSelf",
    ) -> "_2748.ActiveGearSetDesignSelection":
        from mastapy._private.system_model.part_model.gears import _2748

        return self.__parent__._cast(_2748.ActiveGearSetDesignSelection)

    @property
    def active_fe_substructure_selection(
        self: "CastSelf",
    ) -> "_2857.ActiveFESubstructureSelection":
        from mastapy._private.system_model.part_model.configurations import _2857

        return self.__parent__._cast(_2857.ActiveFESubstructureSelection)

    @property
    def active_shaft_design_selection(
        self: "CastSelf",
    ) -> "_2859.ActiveShaftDesignSelection":
        from mastapy._private.system_model.part_model.configurations import _2859

        return self.__parent__._cast(_2859.ActiveShaftDesignSelection)

    @property
    def bearing_detail_selection(self: "CastSelf") -> "_2862.BearingDetailSelection":
        from mastapy._private.system_model.part_model.configurations import _2862

        return self.__parent__._cast(_2862.BearingDetailSelection)

    @property
    def part_detail_selection(self: "CastSelf") -> "PartDetailSelection":
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
class PartDetailSelection(_0.APIBase, Generic[TPart, TSelectableItem]):
    """PartDetailSelection

    This is a mastapy class.

    Generic Types:
        TPart
        TSelectableItem
    """

    TYPE: ClassVar["Type"] = _PART_DETAIL_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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

    @property
    @exception_bridge
    def selection(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_TSelectableItem":
        """ListWithSelectedItem[TSelectableItem]"""
        temp = pythonnet_property_get(self.wrapped, "Selection")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_TSelectableItem",
        )(temp)

    @selection.setter
    @exception_bridge
    @enforce_parameter_types
    def selection(self: "Self", value: "TSelectableItem") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_TSelectableItem.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Selection", value)

    @property
    @exception_bridge
    def part(self: "Self") -> "TPart":
        """TPart

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Part")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def selected_item(self: "Self") -> "TSelectableItem":
        """TSelectableItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedItem")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_PartDetailSelection":
        """Cast to another type.

        Returns:
            _Cast_PartDetailSelection
        """
        return _Cast_PartDetailSelection(self)
