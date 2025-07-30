"""FENodeSelectionDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, overridable_enum_runtime, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item_and_image
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.dev_tools_analyses import _280

_FE_NODE_SELECTION_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "FENodeSelectionDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="FENodeSelectionDrawStyle")
    CastSelf = TypeVar(
        "CastSelf", bound="FENodeSelectionDrawStyle._Cast_FENodeSelectionDrawStyle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FENodeSelectionDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FENodeSelectionDrawStyle:
    """Special nested class for casting FENodeSelectionDrawStyle to subclasses."""

    __parent__: "FENodeSelectionDrawStyle"

    @property
    def fe_node_selection_draw_style(self: "CastSelf") -> "FENodeSelectionDrawStyle":
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
class FENodeSelectionDrawStyle(_0.APIBase):
    """FENodeSelectionDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_NODE_SELECTION_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def add_to_selection(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "AddToSelection")

        if temp is None:
            return False

        return temp

    @add_to_selection.setter
    @exception_bridge
    @enforce_parameter_types
    def add_to_selection(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "AddToSelection", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def degree(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Degree")

        if temp is None:
            return 0

        return temp

    @degree.setter
    @exception_bridge
    @enforce_parameter_types
    def degree(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Degree", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def include_neighbouring_faces(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeNeighbouringFaces")

        if temp is None:
            return False

        return temp

    @include_neighbouring_faces.setter
    @exception_bridge
    @enforce_parameter_types
    def include_neighbouring_faces(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeNeighbouringFaces",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def region_size(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RegionSize")

        if temp is None:
            return 0.0

        return temp

    @region_size.setter
    @exception_bridge
    @enforce_parameter_types
    def region_size(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RegionSize", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def selection_mode(
        self: "Self",
    ) -> (
        "list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESelectionMode"
    ):
        """ListWithSelectedItemAndImage[mastapy.nodal_analysis.dev_tools_analyses.FESelectionMode]"""
        temp = pythonnet_property_get(self.wrapped, "SelectionMode")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESelectionMode.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @selection_mode.setter
    @exception_bridge
    @enforce_parameter_types
    def selection_mode(self: "Self", value: "_280.FESelectionMode") -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESelectionMode.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "SelectionMode", value)

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
    def clear_selection(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearSelection")

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
    def cast_to(self: "Self") -> "_Cast_FENodeSelectionDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_FENodeSelectionDrawStyle
        """
        return _Cast_FENodeSelectionDrawStyle(self)
