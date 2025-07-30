"""HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_LOCATION_WITHIN_A_HARMONIC = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6165,
        _6166,
        _6169,
        _6170,
    )

    Self = TypeVar(
        "Self", bound="HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic._Cast_HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic:
    """Special nested class for casting HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic to subclasses."""

    __parent__: "HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic"

    @property
    def harmonic_analysis_combined_for_multiple_surfaces_within_a_harmonic(
        self: "CastSelf",
    ) -> "_6165.HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6165,
        )

        return self.__parent__._cast(
            _6165.HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic
        )

    @property
    def harmonic_analysis_results_broken_down_by_component_within_a_harmonic(
        self: "CastSelf",
    ) -> "_6166.HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6166,
        )

        return self.__parent__._cast(
            _6166.HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic
        )

    @property
    def harmonic_analysis_results_broken_down_by_node_within_a_harmonic(
        self: "CastSelf",
    ) -> "_6169.HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6169,
        )

        return self.__parent__._cast(
            _6169.HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic
        )

    @property
    def harmonic_analysis_results_broken_down_by_surface_within_a_harmonic(
        self: "CastSelf",
    ) -> "_6170.HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6170,
        )

        return self.__parent__._cast(
            _6170.HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic
        )

    @property
    def harmonic_analysis_results_broken_down_by_location_within_a_harmonic(
        self: "CastSelf",
    ) -> "HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic":
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
class HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic(_0.APIBase):
    """HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_LOCATION_WITHIN_A_HARMONIC
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic
        """
        return _Cast_HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic(self)
