"""ParametricStudyToolResultsForReporting"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_PARAMETRIC_STUDY_TOOL_RESULTS_FOR_REPORTING = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyToolResultsForReporting",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="ParametricStudyToolResultsForReporting")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ParametricStudyToolResultsForReporting._Cast_ParametricStudyToolResultsForReporting",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyToolResultsForReporting",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParametricStudyToolResultsForReporting:
    """Special nested class for casting ParametricStudyToolResultsForReporting to subclasses."""

    __parent__: "ParametricStudyToolResultsForReporting"

    @property
    def parametric_study_tool_results_for_reporting(
        self: "CastSelf",
    ) -> "ParametricStudyToolResultsForReporting":
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
class ParametricStudyToolResultsForReporting(_0.APIBase):
    """ParametricStudyToolResultsForReporting

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARAMETRIC_STUDY_TOOL_RESULTS_FOR_REPORTING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    @enforce_parameter_types
    def export_results_to_xml(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "ExportResultsToXML", file_path)

    @property
    def cast_to(self: "Self") -> "_Cast_ParametricStudyToolResultsForReporting":
        """Cast to another type.

        Returns:
            _Cast_ParametricStudyToolResultsForReporting
        """
        return _Cast_ParametricStudyToolResultsForReporting(self)
