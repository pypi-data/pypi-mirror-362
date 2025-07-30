"""AbstractAnalysisOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

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

_ABSTRACT_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases",
    "AbstractAnalysisOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6043,
        _6107,
        _6114,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
        _6148,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5746
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4904
    from mastapy._private.system_model.analyses_and_results.static_loads import _7673
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3070,
    )

    Self = TypeVar("Self", bound="AbstractAnalysisOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractAnalysisOptions._Cast_AbstractAnalysisOptions"
    )

T = TypeVar("T", bound="_7673.LoadCase")

__docformat__ = "restructuredtext en"
__all__ = ("AbstractAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAnalysisOptions:
    """Special nested class for casting AbstractAnalysisOptions to subclasses."""

    __parent__: "AbstractAnalysisOptions"

    @property
    def system_deflection_options(self: "CastSelf") -> "_3070.SystemDeflectionOptions":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3070,
        )

        return self.__parent__._cast(_3070.SystemDeflectionOptions)

    @property
    def frequency_response_analysis_options(
        self: "CastSelf",
    ) -> "_4904.FrequencyResponseAnalysisOptions":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4904,
        )

        return self.__parent__._cast(_4904.FrequencyResponseAnalysisOptions)

    @property
    def mbd_run_up_analysis_options(
        self: "CastSelf",
    ) -> "_5746.MBDRunUpAnalysisOptions":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5746,
        )

        return self.__parent__._cast(_5746.MBDRunUpAnalysisOptions)

    @property
    def frequency_options_for_harmonic_analysis_results(
        self: "CastSelf",
    ) -> "_6043.FrequencyOptionsForHarmonicAnalysisResults":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6043,
        )

        return self.__parent__._cast(_6043.FrequencyOptionsForHarmonicAnalysisResults)

    @property
    def speed_options_for_harmonic_analysis_results(
        self: "CastSelf",
    ) -> "_6107.SpeedOptionsForHarmonicAnalysisResults":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6107,
        )

        return self.__parent__._cast(_6107.SpeedOptionsForHarmonicAnalysisResults)

    @property
    def stiffness_options_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6114.StiffnessOptionsForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6114,
        )

        return self.__parent__._cast(_6114.StiffnessOptionsForHarmonicAnalysis)

    @property
    def transfer_path_analysis_setup_options(
        self: "CastSelf",
    ) -> "_6148.TransferPathAnalysisSetupOptions":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
            _6148,
        )

        return self.__parent__._cast(_6148.TransferPathAnalysisSetupOptions)

    @property
    def abstract_analysis_options(self: "CastSelf") -> "AbstractAnalysisOptions":
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
class AbstractAnalysisOptions(_0.APIBase, Generic[T]):
    """AbstractAnalysisOptions

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ANALYSIS_OPTIONS

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
    def cast_to(self: "Self") -> "_Cast_AbstractAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_AbstractAnalysisOptions
        """
        return _Cast_AbstractAnalysisOptions(self)
