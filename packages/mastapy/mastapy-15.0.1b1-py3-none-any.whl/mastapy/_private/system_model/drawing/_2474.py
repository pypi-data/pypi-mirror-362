"""PartAnalysisCaseWithContourViewable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.enums import _2020, _2021

_PART_ANALYSIS_CASE_WITH_CONTOUR_VIEWABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "PartAnalysisCaseWithContourViewable"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.drawing import (
        _2464,
        _2465,
        _2467,
        _2469,
        _2470,
        _2472,
        _2481,
    )

    Self = TypeVar("Self", bound="PartAnalysisCaseWithContourViewable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartAnalysisCaseWithContourViewable._Cast_PartAnalysisCaseWithContourViewable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartAnalysisCaseWithContourViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartAnalysisCaseWithContourViewable:
    """Special nested class for casting PartAnalysisCaseWithContourViewable to subclasses."""

    __parent__: "PartAnalysisCaseWithContourViewable"

    @property
    def abstract_system_deflection_viewable(
        self: "CastSelf",
    ) -> "_2464.AbstractSystemDeflectionViewable":
        from mastapy._private.system_model.drawing import _2464

        return self.__parent__._cast(_2464.AbstractSystemDeflectionViewable)

    @property
    def advanced_system_deflection_viewable(
        self: "CastSelf",
    ) -> "_2465.AdvancedSystemDeflectionViewable":
        from mastapy._private.system_model.drawing import _2465

        return self.__parent__._cast(_2465.AdvancedSystemDeflectionViewable)

    @property
    def dynamic_analysis_viewable(self: "CastSelf") -> "_2469.DynamicAnalysisViewable":
        from mastapy._private.system_model.drawing import _2469

        return self.__parent__._cast(_2469.DynamicAnalysisViewable)

    @property
    def harmonic_analysis_viewable(
        self: "CastSelf",
    ) -> "_2470.HarmonicAnalysisViewable":
        from mastapy._private.system_model.drawing import _2470

        return self.__parent__._cast(_2470.HarmonicAnalysisViewable)

    @property
    def modal_analysis_viewable(self: "CastSelf") -> "_2472.ModalAnalysisViewable":
        from mastapy._private.system_model.drawing import _2472

        return self.__parent__._cast(_2472.ModalAnalysisViewable)

    @property
    def system_deflection_viewable(
        self: "CastSelf",
    ) -> "_2481.SystemDeflectionViewable":
        from mastapy._private.system_model.drawing import _2481

        return self.__parent__._cast(_2481.SystemDeflectionViewable)

    @property
    def part_analysis_case_with_contour_viewable(
        self: "CastSelf",
    ) -> "PartAnalysisCaseWithContourViewable":
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
class PartAnalysisCaseWithContourViewable(_0.APIBase):
    """PartAnalysisCaseWithContourViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_ANALYSIS_CASE_WITH_CONTOUR_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contour(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection":
        """EnumWithSelectedValue[mastapy.utility.enums.ThreeDViewContourOptionFirstSelection]"""
        temp = pythonnet_property_get(self.wrapped, "Contour")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @contour.setter
    @exception_bridge
    @enforce_parameter_types
    def contour(
        self: "Self", value: "_2020.ThreeDViewContourOptionFirstSelection"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Contour", value)

    @property
    @exception_bridge
    def contour_secondary(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection":
        """EnumWithSelectedValue[mastapy.utility.enums.ThreeDViewContourOptionSecondSelection]"""
        temp = pythonnet_property_get(self.wrapped, "ContourSecondary")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @contour_secondary.setter
    @exception_bridge
    @enforce_parameter_types
    def contour_secondary(
        self: "Self", value: "_2021.ThreeDViewContourOptionSecondSelection"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ContourSecondary", value)

    @property
    @exception_bridge
    def contour_draw_style(self: "Self") -> "_2467.ContourDrawStyle":
        """mastapy.system_model.drawing.ContourDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContourDrawStyle")

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
    def cast_to(self: "Self") -> "_Cast_PartAnalysisCaseWithContourViewable":
        """Cast to another type.

        Returns:
            _Cast_PartAnalysisCaseWithContourViewable
        """
        return _Cast_PartAnalysisCaseWithContourViewable(self)
