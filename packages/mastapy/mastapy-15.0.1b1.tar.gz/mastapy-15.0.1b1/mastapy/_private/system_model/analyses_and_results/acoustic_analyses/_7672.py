"""UnitForceExcitationAnalysisDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.acoustic_analyses import _7670

_UNIT_FORCE_EXCITATION_ANALYSIS_DETAIL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses",
    "UnitForceExcitationAnalysisDetail",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="UnitForceExcitationAnalysisDetail")
    CastSelf = TypeVar(
        "CastSelf",
        bound="UnitForceExcitationAnalysisDetail._Cast_UnitForceExcitationAnalysisDetail",
    )


__docformat__ = "restructuredtext en"
__all__ = ("UnitForceExcitationAnalysisDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_UnitForceExcitationAnalysisDetail:
    """Special nested class for casting UnitForceExcitationAnalysisDetail to subclasses."""

    __parent__: "UnitForceExcitationAnalysisDetail"

    @property
    def single_excitation_details(self: "CastSelf") -> "_7670.SingleExcitationDetails":
        return self.__parent__._cast(_7670.SingleExcitationDetails)

    @property
    def unit_force_excitation_analysis_detail(
        self: "CastSelf",
    ) -> "UnitForceExcitationAnalysisDetail":
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
class UnitForceExcitationAnalysisDetail(_7670.SingleExcitationDetails):
    """UnitForceExcitationAnalysisDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _UNIT_FORCE_EXCITATION_ANALYSIS_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_UnitForceExcitationAnalysisDetail":
        """Cast to another type.

        Returns:
            _Cast_UnitForceExcitationAnalysisDetail
        """
        return _Cast_UnitForceExcitationAnalysisDetail(self)
