"""EdgeSelector"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_EDGE_SELECTOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "EdgeSelector"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="EdgeSelector")
    CastSelf = TypeVar("CastSelf", bound="EdgeSelector._Cast_EdgeSelector")


__docformat__ = "restructuredtext en"
__all__ = ("EdgeSelector",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_EdgeSelector:
    """Special nested class for casting EdgeSelector to subclasses."""

    __parent__: "EdgeSelector"

    @property
    def edge_selector(self: "CastSelf") -> "EdgeSelector":
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
class EdgeSelector(_0.APIBase):
    """EdgeSelector

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EDGE_SELECTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def specify_edge_indices(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyEdgeIndices")

        if temp is None:
            return False

        return temp

    @specify_edge_indices.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_edge_indices(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyEdgeIndices",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def number_of_rotor_edges(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfRotorEdges")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def selected_edge_indices(self: "Self") -> "List[int]":
        """List[int]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedEdgeIndices")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, int)

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
    def set_edge_indices(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetEdgeIndices")

    @exception_bridge
    @enforce_parameter_types
    def set_selected_edge_indices(
        self: "Self", zero_based_edge_indices: "List[int]"
    ) -> None:
        """Method does not return.

        Args:
            zero_based_edge_indices (List[int])
        """
        zero_based_edge_indices = conversion.mp_to_pn_objects_in_list(
            zero_based_edge_indices
        )
        pythonnet_method_call(
            self.wrapped, "SetSelectedEdgeIndices", zero_based_edge_indices
        )

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
    def cast_to(self: "Self") -> "_Cast_EdgeSelector":
        """Cast to another type.

        Returns:
            _Cast_EdgeSelector
        """
        return _Cast_EdgeSelector(self)
