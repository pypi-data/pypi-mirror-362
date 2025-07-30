"""ResultLocationSelectionGroups"""

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
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results import (
    _6157,
)

_RESULT_LOCATION_SELECTION_GROUPS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results",
    "ResultLocationSelectionGroups",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="ResultLocationSelectionGroups")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ResultLocationSelectionGroups._Cast_ResultLocationSelectionGroups",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultLocationSelectionGroups",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultLocationSelectionGroups:
    """Special nested class for casting ResultLocationSelectionGroups to subclasses."""

    __parent__: "ResultLocationSelectionGroups"

    @property
    def result_location_selection_groups(
        self: "CastSelf",
    ) -> "ResultLocationSelectionGroups":
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
class ResultLocationSelectionGroups(_0.APIBase):
    """ResultLocationSelectionGroups

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESULT_LOCATION_SELECTION_GROUPS

    class DisplayLocationSelectionOption(Enum):
        """DisplayLocationSelectionOption is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _RESULT_LOCATION_SELECTION_GROUPS.DisplayLocationSelectionOption

        CURRENT_ITEM = 0
        GROUPS = 1

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    DisplayLocationSelectionOption.__setattr__ = __enum_setattr
    DisplayLocationSelectionOption.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def display_location_selection(
        self: "Self",
    ) -> "ResultLocationSelectionGroups.DisplayLocationSelectionOption":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.results.ResultLocationSelectionGroups.DisplayLocationSelectionOption"""
        temp = pythonnet_property_get(self.wrapped, "DisplayLocationSelection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results.ResultLocationSelectionGroups+DisplayLocationSelectionOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.harmonic_analyses.results.ResultLocationSelectionGroups.ResultLocationSelectionGroups",
            "DisplayLocationSelectionOption",
        )(value)

    @display_location_selection.setter
    @exception_bridge
    @enforce_parameter_types
    def display_location_selection(
        self: "Self",
        value: "ResultLocationSelectionGroups.DisplayLocationSelectionOption",
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results.ResultLocationSelectionGroups+DisplayLocationSelectionOption",
        )
        pythonnet_property_set(self.wrapped, "DisplayLocationSelection", value)

    @property
    @exception_bridge
    def select_result_location_group(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_ResultLocationSelectionGroup":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.harmonic_analyses.results.ResultLocationSelectionGroup]"""
        temp = pythonnet_property_get(self.wrapped, "SelectResultLocationGroup")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_ResultLocationSelectionGroup",
        )(temp)

    @select_result_location_group.setter
    @exception_bridge
    @enforce_parameter_types
    def select_result_location_group(
        self: "Self", value: "_6157.ResultLocationSelectionGroup"
    ) -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_ResultLocationSelectionGroup.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "SelectResultLocationGroup", value)

    @property
    @exception_bridge
    def selected_result_location_group(
        self: "Self",
    ) -> "_6157.ResultLocationSelectionGroup":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.results.ResultLocationSelectionGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedResultLocationGroup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def result_location_groups(
        self: "Self",
    ) -> "List[_6157.ResultLocationSelectionGroup]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.results.ResultLocationSelectionGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultLocationGroups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def add_new_group(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddNewGroup")

    @exception_bridge
    def remove_groups(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveGroups")

    @exception_bridge
    def view_groups(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ViewGroups")

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
    def cast_to(self: "Self") -> "_Cast_ResultLocationSelectionGroups":
        """Cast to another type.

        Returns:
            _Cast_ResultLocationSelectionGroups
        """
        return _Cast_ResultLocationSelectionGroups(self)
