"""ResultsForOrder"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_RESULTS_FOR_ORDER = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "ResultsForOrder",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6166,
        _6176,
        _6177,
        _6178,
    )

    Self = TypeVar("Self", bound="ResultsForOrder")
    CastSelf = TypeVar("CastSelf", bound="ResultsForOrder._Cast_ResultsForOrder")


__docformat__ = "restructuredtext en"
__all__ = ("ResultsForOrder",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultsForOrder:
    """Special nested class for casting ResultsForOrder to subclasses."""

    __parent__: "ResultsForOrder"

    @property
    def results_for_order_including_groups(
        self: "CastSelf",
    ) -> "_6176.ResultsForOrderIncludingGroups":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6176,
        )

        return self.__parent__._cast(_6176.ResultsForOrderIncludingGroups)

    @property
    def results_for_order_including_nodes(
        self: "CastSelf",
    ) -> "_6177.ResultsForOrderIncludingNodes":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6177,
        )

        return self.__parent__._cast(_6177.ResultsForOrderIncludingNodes)

    @property
    def results_for_order_including_surfaces(
        self: "CastSelf",
    ) -> "_6178.ResultsForOrderIncludingSurfaces":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6178,
        )

        return self.__parent__._cast(_6178.ResultsForOrderIncludingSurfaces)

    @property
    def results_for_order(self: "CastSelf") -> "ResultsForOrder":
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
class ResultsForOrder(_0.APIBase):
    """ResultsForOrder

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESULTS_FOR_ORDER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def excitations_description(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcitationsDescription")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def harmonics(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Harmonics")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def order(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Order")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def component(
        self: "Self",
    ) -> "_6166.HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Component")

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
    def cast_to(self: "Self") -> "_Cast_ResultsForOrder":
        """Cast to another type.

        Returns:
            _Cast_ResultsForOrder
        """
        return _Cast_ResultsForOrder(self)
