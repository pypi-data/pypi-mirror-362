"""CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5289,
)

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5176,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5268,
        _5300,
        _5364,
    )

    Self = TypeVar(
        "Self",
        bound="CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness._Cast_CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness"

    @property
    def coaxial_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5289.CoaxialConnectionCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(
            _5289.CoaxialConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def shaft_to_mountable_component_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5364.ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5364,
        )

        return self.__parent__._cast(
            _5364.ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5268.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5268,
        )

        return self.__parent__._cast(
            _5268.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5300.ConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5300,
        )

        return self.__parent__._cast(_5300.ConnectionCompoundModalAnalysisAtAStiffness)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7881.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7881,
        )

        return self.__parent__._cast(_7881.ConnectionCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7885.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7885,
        )

        return self.__parent__._cast(_7885.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness":
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
class CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness(
    _5289.CoaxialConnectionCompoundModalAnalysisAtAStiffness
):
    """CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5176.CycloidalDiscCentralBearingConnectionModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.CycloidalDiscCentralBearingConnectionModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5176.CycloidalDiscCentralBearingConnectionModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.CycloidalDiscCentralBearingConnectionModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness
        """
        return _Cast_CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness(
            self
        )
