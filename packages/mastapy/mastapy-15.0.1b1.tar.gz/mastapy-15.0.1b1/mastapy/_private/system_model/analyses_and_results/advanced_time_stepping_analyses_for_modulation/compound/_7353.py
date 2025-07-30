"""RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
    _7326,
)

_RING_PINS_TO_DISC_CONNECTION_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound",
    "RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7222,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
        _7296,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2562

    Self = TypeVar(
        "Self",
        bound="RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: (
        "RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
    )

    @property
    def inter_mountable_component_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7326.InterMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7326.InterMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7296.ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7296,
        )

        return self.__parent__._cast(
            _7296.ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

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
    def ring_pins_to_disc_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
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
class RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation(
    _7326.InterMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
):
    """RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _RING_PINS_TO_DISC_CONNECTION_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2562.RingPinsToDiscConnection":
        """mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2562.RingPinsToDiscConnection":
        """mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> (
        "List[_7222.RingPinsToDiscConnectionAdvancedTimeSteppingAnalysisForModulation]"
    ):
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.RingPinsToDiscConnectionAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> (
        "List[_7222.RingPinsToDiscConnectionAdvancedTimeSteppingAnalysisForModulation]"
    ):
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.RingPinsToDiscConnectionAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> "_Cast_RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation(
            self
        )
