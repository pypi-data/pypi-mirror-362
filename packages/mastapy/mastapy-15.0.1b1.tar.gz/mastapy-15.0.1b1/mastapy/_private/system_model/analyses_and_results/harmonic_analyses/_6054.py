"""HarmonicAnalysisDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6642

_HARMONIC_ANALYSIS_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "HarmonicAnalysisDrawStyle",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.geometry import _397
    from mastapy._private.system_model.drawing import _2467

    Self = TypeVar("Self", bound="HarmonicAnalysisDrawStyle")
    CastSelf = TypeVar(
        "CastSelf", bound="HarmonicAnalysisDrawStyle._Cast_HarmonicAnalysisDrawStyle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisDrawStyle:
    """Special nested class for casting HarmonicAnalysisDrawStyle to subclasses."""

    __parent__: "HarmonicAnalysisDrawStyle"

    @property
    def dynamic_analysis_draw_style(
        self: "CastSelf",
    ) -> "_6642.DynamicAnalysisDrawStyle":
        return self.__parent__._cast(_6642.DynamicAnalysisDrawStyle)

    @property
    def contour_draw_style(self: "CastSelf") -> "_2467.ContourDrawStyle":
        from mastapy._private.system_model.drawing import _2467

        return self.__parent__._cast(_2467.ContourDrawStyle)

    @property
    def draw_style_base(self: "CastSelf") -> "_397.DrawStyleBase":
        from mastapy._private.geometry import _397

        return self.__parent__._cast(_397.DrawStyleBase)

    @property
    def harmonic_analysis_draw_style(self: "CastSelf") -> "HarmonicAnalysisDrawStyle":
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
class HarmonicAnalysisDrawStyle(_6642.DynamicAnalysisDrawStyle):
    """HarmonicAnalysisDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ANALYSIS_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicAnalysisDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisDrawStyle
        """
        return _Cast_HarmonicAnalysisDrawStyle(self)
