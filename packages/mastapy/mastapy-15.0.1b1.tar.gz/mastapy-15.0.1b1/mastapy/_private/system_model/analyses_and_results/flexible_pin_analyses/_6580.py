"""CombinationAnalysis"""

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

_COMBINATION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses",
    "CombinationAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
        _6581,
        _6582,
        _6583,
        _6584,
        _6585,
        _6587,
        _6588,
    )

    Self = TypeVar("Self", bound="CombinationAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="CombinationAnalysis._Cast_CombinationAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CombinationAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CombinationAnalysis:
    """Special nested class for casting CombinationAnalysis to subclasses."""

    __parent__: "CombinationAnalysis"

    @property
    def flexible_pin_analysis(self: "CastSelf") -> "_6581.FlexiblePinAnalysis":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6581,
        )

        return self.__parent__._cast(_6581.FlexiblePinAnalysis)

    @property
    def flexible_pin_analysis_concept_level(
        self: "CastSelf",
    ) -> "_6582.FlexiblePinAnalysisConceptLevel":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6582,
        )

        return self.__parent__._cast(_6582.FlexiblePinAnalysisConceptLevel)

    @property
    def flexible_pin_analysis_detail_level_and_pin_fatigue_one_tooth_pass(
        self: "CastSelf",
    ) -> "_6583.FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6583,
        )

        return self.__parent__._cast(
            _6583.FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass
        )

    @property
    def flexible_pin_analysis_gear_and_bearing_rating(
        self: "CastSelf",
    ) -> "_6584.FlexiblePinAnalysisGearAndBearingRating":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6584,
        )

        return self.__parent__._cast(_6584.FlexiblePinAnalysisGearAndBearingRating)

    @property
    def flexible_pin_analysis_manufacture_level(
        self: "CastSelf",
    ) -> "_6585.FlexiblePinAnalysisManufactureLevel":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6585,
        )

        return self.__parent__._cast(_6585.FlexiblePinAnalysisManufactureLevel)

    @property
    def flexible_pin_analysis_stop_start_analysis(
        self: "CastSelf",
    ) -> "_6587.FlexiblePinAnalysisStopStartAnalysis":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6587,
        )

        return self.__parent__._cast(_6587.FlexiblePinAnalysisStopStartAnalysis)

    @property
    def wind_turbine_certification_report(
        self: "CastSelf",
    ) -> "_6588.WindTurbineCertificationReport":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6588,
        )

        return self.__parent__._cast(_6588.WindTurbineCertificationReport)

    @property
    def combination_analysis(self: "CastSelf") -> "CombinationAnalysis":
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
class CombinationAnalysis(_0.APIBase):
    """CombinationAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMBINATION_ANALYSIS

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
    def cast_to(self: "Self") -> "_Cast_CombinationAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CombinationAnalysis
        """
        return _Cast_CombinationAnalysis(self)
