"""SingleHarmonicExcitationAnalysisDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.acoustic_analyses import _7670

_SINGLE_HARMONIC_EXCITATION_ANALYSIS_DETAIL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses",
    "SingleHarmonicExcitationAnalysisDetail",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SingleHarmonicExcitationAnalysisDetail")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SingleHarmonicExcitationAnalysisDetail._Cast_SingleHarmonicExcitationAnalysisDetail",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SingleHarmonicExcitationAnalysisDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SingleHarmonicExcitationAnalysisDetail:
    """Special nested class for casting SingleHarmonicExcitationAnalysisDetail to subclasses."""

    __parent__: "SingleHarmonicExcitationAnalysisDetail"

    @property
    def single_excitation_details(self: "CastSelf") -> "_7670.SingleExcitationDetails":
        return self.__parent__._cast(_7670.SingleExcitationDetails)

    @property
    def single_harmonic_excitation_analysis_detail(
        self: "CastSelf",
    ) -> "SingleHarmonicExcitationAnalysisDetail":
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
class SingleHarmonicExcitationAnalysisDetail(_7670.SingleExcitationDetails):
    """SingleHarmonicExcitationAnalysisDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SINGLE_HARMONIC_EXCITATION_ANALYSIS_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SingleHarmonicExcitationAnalysisDetail":
        """Cast to another type.

        Returns:
            _Cast_SingleHarmonicExcitationAnalysisDetail
        """
        return _Cast_SingleHarmonicExcitationAnalysisDetail(self)
