"""UserSpecifiedEdgeIndices"""

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

_USER_SPECIFIED_EDGE_INDICES = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "UserSpecifiedEdgeIndices"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="UserSpecifiedEdgeIndices")
    CastSelf = TypeVar(
        "CastSelf", bound="UserSpecifiedEdgeIndices._Cast_UserSpecifiedEdgeIndices"
    )


__docformat__ = "restructuredtext en"
__all__ = ("UserSpecifiedEdgeIndices",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_UserSpecifiedEdgeIndices:
    """Special nested class for casting UserSpecifiedEdgeIndices to subclasses."""

    __parent__: "UserSpecifiedEdgeIndices"

    @property
    def user_specified_edge_indices(self: "CastSelf") -> "UserSpecifiedEdgeIndices":
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
class UserSpecifiedEdgeIndices(_0.APIBase):
    """UserSpecifiedEdgeIndices

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _USER_SPECIFIED_EDGE_INDICES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def inner_edge_indices(self: "Self") -> "Tuple[int, int]":
        """Tuple[int, int]"""
        temp = pythonnet_property_get(self.wrapped, "InnerEdgeIndices")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @inner_edge_indices.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_edge_indices(self: "Self", value: "Tuple[int, int]") -> None:
        value = conversion.mp_to_pn_integer_range(value)
        pythonnet_property_set(self.wrapped, "InnerEdgeIndices", value)

    @property
    @exception_bridge
    def outer_edge_indices(self: "Self") -> "Tuple[int, int]":
        """Tuple[int, int]"""
        temp = pythonnet_property_get(self.wrapped, "OuterEdgeIndices")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @outer_edge_indices.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_edge_indices(self: "Self", value: "Tuple[int, int]") -> None:
        value = conversion.mp_to_pn_integer_range(value)
        pythonnet_property_set(self.wrapped, "OuterEdgeIndices", value)

    @property
    @exception_bridge
    def region_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RegionName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def side_edge_indices(self: "Self") -> "Tuple[int, int]":
        """Tuple[int, int]"""
        temp = pythonnet_property_get(self.wrapped, "SideEdgeIndices")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @side_edge_indices.setter
    @exception_bridge
    @enforce_parameter_types
    def side_edge_indices(self: "Self", value: "Tuple[int, int]") -> None:
        value = conversion.mp_to_pn_integer_range(value)
        pythonnet_property_set(self.wrapped, "SideEdgeIndices", value)

    @property
    @exception_bridge
    def specify_edge_indices_for_end_winding_surfaces(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "SpecifyEdgeIndicesForEndWindingSurfaces"
        )

        if temp is None:
            return False

        return temp

    @specify_edge_indices_for_end_winding_surfaces.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_edge_indices_for_end_winding_surfaces(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyEdgeIndicesForEndWindingSurfaces",
            bool(value) if value is not None else False,
        )

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
    def cast_to(self: "Self") -> "_Cast_UserSpecifiedEdgeIndices":
        """Cast to another type.

        Returns:
            _Cast_UserSpecifiedEdgeIndices
        """
        return _Cast_UserSpecifiedEdgeIndices(self)
