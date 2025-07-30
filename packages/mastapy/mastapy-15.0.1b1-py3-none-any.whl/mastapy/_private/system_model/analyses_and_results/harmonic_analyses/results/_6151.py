"""ExcitationSourceSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results import (
    _6152,
)

_EXCITATION_SOURCE_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results",
    "ExcitationSourceSelection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.math_utility import _1713
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results import (
        _6154,
    )

    Self = TypeVar("Self", bound="ExcitationSourceSelection")
    CastSelf = TypeVar(
        "CastSelf", bound="ExcitationSourceSelection._Cast_ExcitationSourceSelection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExcitationSourceSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExcitationSourceSelection:
    """Special nested class for casting ExcitationSourceSelection to subclasses."""

    __parent__: "ExcitationSourceSelection"

    @property
    def excitation_source_selection_base(
        self: "CastSelf",
    ) -> "_6152.ExcitationSourceSelectionBase":
        return self.__parent__._cast(_6152.ExcitationSourceSelectionBase)

    @property
    def excitation_source_selection(self: "CastSelf") -> "ExcitationSourceSelection":
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
class ExcitationSourceSelection(_6152.ExcitationSourceSelectionBase):
    """ExcitationSourceSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXCITATION_SOURCE_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def harmonic_selections(self: "Self") -> "List[_6154.HarmonicSelection]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.results.HarmonicSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicSelections")

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
    def invert_is_included_in_excitations_selection(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "InvertIsIncludedInExcitationsSelection")

    @exception_bridge
    def invert_is_shown_selection(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "InvertIsShownSelection")

    @exception_bridge
    @enforce_parameter_types
    def include_only_harmonic_with_order(
        self: "Self", order: "_1713.RoundedOrder"
    ) -> "bool":
        """bool

        Args:
            order (mastapy.math_utility.RoundedOrder)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "IncludeOnlyHarmonicWithOrder",
            order.wrapped if order else None,
        )
        return method_result

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
    def cast_to(self: "Self") -> "_Cast_ExcitationSourceSelection":
        """Cast to another type.

        Returns:
            _Cast_ExcitationSourceSelection
        """
        return _Cast_ExcitationSourceSelection(self)
