"""ModalContributionViewOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
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

_MODAL_CONTRIBUTION_VIEW_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing.Options", "ModalContributionViewOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results import (
        _6155,
        _6156,
    )

    Self = TypeVar("Self", bound="ModalContributionViewOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ModalContributionViewOptions._Cast_ModalContributionViewOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModalContributionViewOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModalContributionViewOptions:
    """Special nested class for casting ModalContributionViewOptions to subclasses."""

    __parent__: "ModalContributionViewOptions"

    @property
    def modal_contribution_view_options(
        self: "CastSelf",
    ) -> "ModalContributionViewOptions":
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
class ModalContributionViewOptions(_0.APIBase):
    """ModalContributionViewOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODAL_CONTRIBUTION_VIEW_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def filtering_frequency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FilteringFrequency")

        if temp is None:
            return 0.0

        return temp

    @filtering_frequency.setter
    @exception_bridge
    @enforce_parameter_types
    def filtering_frequency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FilteringFrequency",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def filtering_frequency_range(self: "Self") -> "Tuple[float, float]":
        """Tuple[float, float]"""
        temp = pythonnet_property_get(self.wrapped, "FilteringFrequencyRange")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @filtering_frequency_range.setter
    @exception_bridge
    @enforce_parameter_types
    def filtering_frequency_range(self: "Self", value: "Tuple[float, float]") -> None:
        value = conversion.mp_to_pn_range(value)
        pythonnet_property_set(self.wrapped, "FilteringFrequencyRange", value)

    @property
    @exception_bridge
    def filtering_method(self: "Self") -> "_6156.ModalContributionFilteringMethod":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.results.ModalContributionFilteringMethod"""
        temp = pythonnet_property_get(self.wrapped, "FilteringMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results.ModalContributionFilteringMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._6156",
            "ModalContributionFilteringMethod",
        )(value)

    @filtering_method.setter
    @exception_bridge
    @enforce_parameter_types
    def filtering_method(
        self: "Self", value: "_6156.ModalContributionFilteringMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results.ModalContributionFilteringMethod",
        )
        pythonnet_property_set(self.wrapped, "FilteringMethod", value)

    @property
    @exception_bridge
    def frequency_range(self: "Self") -> "Tuple[float, float]":
        """Tuple[float, float]"""
        temp = pythonnet_property_get(self.wrapped, "FrequencyRange")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @frequency_range.setter
    @exception_bridge
    @enforce_parameter_types
    def frequency_range(self: "Self", value: "Tuple[float, float]") -> None:
        value = conversion.mp_to_pn_range(value)
        pythonnet_property_set(self.wrapped, "FrequencyRange", value)

    @property
    @exception_bridge
    def index(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Index")

        if temp is None:
            return 0

        return temp

    @index.setter
    @exception_bridge
    @enforce_parameter_types
    def index(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Index", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def index_range(self: "Self") -> "Tuple[int, int]":
        """Tuple[int, int]"""
        temp = pythonnet_property_get(self.wrapped, "IndexRange")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @index_range.setter
    @exception_bridge
    @enforce_parameter_types
    def index_range(self: "Self", value: "Tuple[int, int]") -> None:
        value = conversion.mp_to_pn_integer_range(value)
        pythonnet_property_set(self.wrapped, "IndexRange", value)

    @property
    @exception_bridge
    def modes_to_display(self: "Self") -> "_6155.ModalContributionDisplayMethod":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.results.ModalContributionDisplayMethod"""
        temp = pythonnet_property_get(self.wrapped, "ModesToDisplay")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results.ModalContributionDisplayMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._6155",
            "ModalContributionDisplayMethod",
        )(value)

    @modes_to_display.setter
    @exception_bridge
    @enforce_parameter_types
    def modes_to_display(
        self: "Self", value: "_6155.ModalContributionDisplayMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results.ModalContributionDisplayMethod",
        )
        pythonnet_property_set(self.wrapped, "ModesToDisplay", value)

    @property
    @exception_bridge
    def percentage_of_total_response(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PercentageOfTotalResponse")

        if temp is None:
            return 0.0

        return temp

    @percentage_of_total_response.setter
    @exception_bridge
    @enforce_parameter_types
    def percentage_of_total_response(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PercentageOfTotalResponse",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def show_modal_contribution(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowModalContribution")

        if temp is None:
            return False

        return temp

    @show_modal_contribution.setter
    @exception_bridge
    @enforce_parameter_types
    def show_modal_contribution(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowModalContribution",
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
    def cast_to(self: "Self") -> "_Cast_ModalContributionViewOptions":
        """Cast to another type.

        Returns:
            _Cast_ModalContributionViewOptions
        """
        return _Cast_ModalContributionViewOptions(self)
