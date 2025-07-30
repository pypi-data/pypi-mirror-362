"""DesignEntityModalAnalysisGroupResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_DESIGN_ENTITY_MODAL_ANALYSIS_GROUP_RESULTS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting",
    "DesignEntityModalAnalysisGroupResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4999,
        _5000,
    )

    Self = TypeVar("Self", bound="DesignEntityModalAnalysisGroupResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DesignEntityModalAnalysisGroupResults._Cast_DesignEntityModalAnalysisGroupResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DesignEntityModalAnalysisGroupResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignEntityModalAnalysisGroupResults:
    """Special nested class for casting DesignEntityModalAnalysisGroupResults to subclasses."""

    __parent__: "DesignEntityModalAnalysisGroupResults"

    @property
    def single_excitation_results_modal_analysis(
        self: "CastSelf",
    ) -> "_4999.SingleExcitationResultsModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4999,
        )

        return self.__parent__._cast(_4999.SingleExcitationResultsModalAnalysis)

    @property
    def single_mode_results(self: "CastSelf") -> "_5000.SingleModeResults":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _5000,
        )

        return self.__parent__._cast(_5000.SingleModeResults)

    @property
    def design_entity_modal_analysis_group_results(
        self: "CastSelf",
    ) -> "DesignEntityModalAnalysisGroupResults":
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
class DesignEntityModalAnalysisGroupResults(_0.APIBase):
    """DesignEntityModalAnalysisGroupResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_ENTITY_MODAL_ANALYSIS_GROUP_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_DesignEntityModalAnalysisGroupResults":
        """Cast to another type.

        Returns:
            _Cast_DesignEntityModalAnalysisGroupResults
        """
        return _Cast_DesignEntityModalAnalysisGroupResults(self)
