"""FEModelHarmonicAnalysisDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.dev_tools_analyses import _277

_FE_MODEL_HARMONIC_ANALYSIS_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "FEModelHarmonicAnalysisDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEModelHarmonicAnalysisDrawStyle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FEModelHarmonicAnalysisDrawStyle._Cast_FEModelHarmonicAnalysisDrawStyle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEModelHarmonicAnalysisDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEModelHarmonicAnalysisDrawStyle:
    """Special nested class for casting FEModelHarmonicAnalysisDrawStyle to subclasses."""

    __parent__: "FEModelHarmonicAnalysisDrawStyle"

    @property
    def fe_model_tab_draw_style(self: "CastSelf") -> "_277.FEModelTabDrawStyle":
        return self.__parent__._cast(_277.FEModelTabDrawStyle)

    @property
    def fe_model_harmonic_analysis_draw_style(
        self: "CastSelf",
    ) -> "FEModelHarmonicAnalysisDrawStyle":
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
class FEModelHarmonicAnalysisDrawStyle(_277.FEModelTabDrawStyle):
    """FEModelHarmonicAnalysisDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_MODEL_HARMONIC_ANALYSIS_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FEModelHarmonicAnalysisDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_FEModelHarmonicAnalysisDrawStyle
        """
        return _Cast_FEModelHarmonicAnalysisDrawStyle(self)
