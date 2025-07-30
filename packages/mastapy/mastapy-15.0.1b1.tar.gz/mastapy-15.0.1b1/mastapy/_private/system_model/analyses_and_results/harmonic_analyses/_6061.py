"""HarmonicAnalysisShaftExportOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results import _2897
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6055
from mastapy._private.system_model.part_model.shaft_model import _2714

_HARMONIC_ANALYSIS_SHAFT_EXPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "HarmonicAnalysisShaftExportOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HarmonicAnalysisShaftExportOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisShaftExportOptions._Cast_HarmonicAnalysisShaftExportOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisShaftExportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisShaftExportOptions:
    """Special nested class for casting HarmonicAnalysisShaftExportOptions to subclasses."""

    __parent__: "HarmonicAnalysisShaftExportOptions"

    @property
    def harmonic_analysis_export_options(
        self: "CastSelf",
    ) -> "_6055.HarmonicAnalysisExportOptions":
        return self.__parent__._cast(_6055.HarmonicAnalysisExportOptions)

    @property
    def harmonic_analysis_shaft_export_options(
        self: "CastSelf",
    ) -> "HarmonicAnalysisShaftExportOptions":
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
class HarmonicAnalysisShaftExportOptions(
    _6055.HarmonicAnalysisExportOptions[_2897.IHaveShaftHarmonicResults, _2714.Shaft]
):
    """HarmonicAnalysisShaftExportOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ANALYSIS_SHAFT_EXPORT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicAnalysisShaftExportOptions":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisShaftExportOptions
        """
        return _Cast_HarmonicAnalysisShaftExportOptions(self)
