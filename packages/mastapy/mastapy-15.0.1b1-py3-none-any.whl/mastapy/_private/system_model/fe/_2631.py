"""RaceBearingFE"""

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
from mastapy._private.system_model.part_model import _2674

_RACE_BEARING_FE = python_net_import("SMT.MastaAPI.SystemModel.FE", "RaceBearingFE")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.fe import _2578, _2585

    Self = TypeVar("Self", bound="RaceBearingFE")
    CastSelf = TypeVar("CastSelf", bound="RaceBearingFE._Cast_RaceBearingFE")


__docformat__ = "restructuredtext en"
__all__ = ("RaceBearingFE",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RaceBearingFE:
    """Special nested class for casting RaceBearingFE to subclasses."""

    __parent__: "RaceBearingFE"

    @property
    def race_bearing_fe(self: "CastSelf") -> "RaceBearingFE":
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
class RaceBearingFE(_0.APIBase):
    """RaceBearingFE

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RACE_BEARING_FE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def alignment_method(self: "Self") -> "_2578.AlignmentMethodForRaceBearing":
        """mastapy.system_model.fe.AlignmentMethodForRaceBearing"""
        temp = pythonnet_property_get(self.wrapped, "AlignmentMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.FE.AlignmentMethodForRaceBearing"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.fe._2578", "AlignmentMethodForRaceBearing"
        )(value)

    @alignment_method.setter
    @exception_bridge
    @enforce_parameter_types
    def alignment_method(
        self: "Self", value: "_2578.AlignmentMethodForRaceBearing"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.FE.AlignmentMethodForRaceBearing"
        )
        pythonnet_property_set(self.wrapped, "AlignmentMethod", value)

    @property
    @exception_bridge
    def datum(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_Datum":
        """ListWithSelectedItem[mastapy.system_model.part_model.Datum]"""
        temp = pythonnet_property_get(self.wrapped, "Datum")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Datum",
        )(temp)

    @datum.setter
    @exception_bridge
    @enforce_parameter_types
    def datum(self: "Self", value: "_2674.Datum") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Datum", value)

    @property
    @exception_bridge
    def fe_filename(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEFilename")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def links(self: "Self") -> "List[_2585.BearingRaceNodeLink]":
        """List[mastapy.system_model.fe.BearingRaceNodeLink]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Links")

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
    def copy_datum_to_manual(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CopyDatumToManual")

    @exception_bridge
    def find_nodes_for_links(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "FindNodesForLinks")

    @exception_bridge
    def import_fe_mesh(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ImportFEMesh")

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
    def cast_to(self: "Self") -> "_Cast_RaceBearingFE":
        """Cast to another type.

        Returns:
            _Cast_RaceBearingFE
        """
        return _Cast_RaceBearingFE(self)
