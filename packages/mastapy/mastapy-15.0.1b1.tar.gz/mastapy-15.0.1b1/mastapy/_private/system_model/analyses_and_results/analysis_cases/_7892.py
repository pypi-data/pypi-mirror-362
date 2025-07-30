"""StaticLoadAnalysisCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7877

_STATIC_LOAD_ANALYSIS_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases",
    "StaticLoadAnalysisCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2891
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7396,
        _7398,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7128,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7879,
        _7886,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6899,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6641,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6023,
        _6052,
        _6057,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
        _6140,
        _6141,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6378,
        _6396,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4895,
        _4926,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5475,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5184,
        _5212,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4385
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4073,
        _4129,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7674
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3280,
        _3336,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3864,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3601,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3068,
        _3075,
    )

    Self = TypeVar("Self", bound="StaticLoadAnalysisCase")
    CastSelf = TypeVar(
        "CastSelf", bound="StaticLoadAnalysisCase._Cast_StaticLoadAnalysisCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StaticLoadAnalysisCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StaticLoadAnalysisCase:
    """Special nested class for casting StaticLoadAnalysisCase to subclasses."""

    __parent__: "StaticLoadAnalysisCase"

    @property
    def analysis_case(self: "CastSelf") -> "_7877.AnalysisCase":
        return self.__parent__._cast(_7877.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2891.Context":
        from mastapy._private.system_model.analyses_and_results import _2891

        return self.__parent__._cast(_2891.Context)

    @property
    def system_deflection(self: "CastSelf") -> "_3068.SystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3068,
        )

        return self.__parent__._cast(_3068.SystemDeflection)

    @property
    def torsional_system_deflection(
        self: "CastSelf",
    ) -> "_3075.TorsionalSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3075,
        )

        return self.__parent__._cast(_3075.TorsionalSystemDeflection)

    @property
    def dynamic_model_for_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3280.DynamicModelForSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3280,
        )

        return self.__parent__._cast(
            _3280.DynamicModelForSteadyStateSynchronousResponse
        )

    @property
    def steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3336.SteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3336,
        )

        return self.__parent__._cast(_3336.SteadyStateSynchronousResponse)

    @property
    def steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3601.SteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3601,
        )

        return self.__parent__._cast(_3601.SteadyStateSynchronousResponseOnAShaft)

    @property
    def steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3864.SteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3864,
        )

        return self.__parent__._cast(_3864.SteadyStateSynchronousResponseAtASpeed)

    @property
    def dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "_4073.DynamicModelForStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4073,
        )

        return self.__parent__._cast(_4073.DynamicModelForStabilityAnalysis)

    @property
    def stability_analysis(self: "CastSelf") -> "_4129.StabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4129,
        )

        return self.__parent__._cast(_4129.StabilityAnalysis)

    @property
    def power_flow(self: "CastSelf") -> "_4385.PowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4385

        return self.__parent__._cast(_4385.PowerFlow)

    @property
    def dynamic_model_for_modal_analysis(
        self: "CastSelf",
    ) -> "_4895.DynamicModelForModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4895,
        )

        return self.__parent__._cast(_4895.DynamicModelForModalAnalysis)

    @property
    def modal_analysis(self: "CastSelf") -> "_4926.ModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4926,
        )

        return self.__parent__._cast(_4926.ModalAnalysis)

    @property
    def dynamic_model_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5184.DynamicModelAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5184,
        )

        return self.__parent__._cast(_5184.DynamicModelAtAStiffness)

    @property
    def modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5212.ModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5212,
        )

        return self.__parent__._cast(_5212.ModalAnalysisAtAStiffness)

    @property
    def modal_analysis_at_a_speed(self: "CastSelf") -> "_5475.ModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5475,
        )

        return self.__parent__._cast(_5475.ModalAnalysisAtASpeed)

    @property
    def dynamic_model_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6023.DynamicModelForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6023,
        )

        return self.__parent__._cast(_6023.DynamicModelForHarmonicAnalysis)

    @property
    def harmonic_analysis(self: "CastSelf") -> "_6052.HarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6052,
        )

        return self.__parent__._cast(_6052.HarmonicAnalysis)

    @property
    def harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_6057.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6057,
        )

        return self.__parent__._cast(
            _6057.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def dynamic_model_for_transfer_path_analysis(
        self: "CastSelf",
    ) -> "_6140.DynamicModelForTransferPathAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
            _6140,
        )

        return self.__parent__._cast(_6140.DynamicModelForTransferPathAnalysis)

    @property
    def modal_analysis_for_transfer_path_analysis(
        self: "CastSelf",
    ) -> "_6141.ModalAnalysisForTransferPathAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
            _6141,
        )

        return self.__parent__._cast(_6141.ModalAnalysisForTransferPathAnalysis)

    @property
    def harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6378.HarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6378,
        )

        return self.__parent__._cast(_6378.HarmonicAnalysisOfSingleExcitation)

    @property
    def modal_analysis_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6396.ModalAnalysisForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6396,
        )

        return self.__parent__._cast(_6396.ModalAnalysisForHarmonicAnalysis)

    @property
    def dynamic_analysis(self: "CastSelf") -> "_6641.DynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6641,
        )

        return self.__parent__._cast(_6641.DynamicAnalysis)

    @property
    def critical_speed_analysis(self: "CastSelf") -> "_6899.CriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6899,
        )

        return self.__parent__._cast(_6899.CriticalSpeedAnalysis)

    @property
    def advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7128.AdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7128,
        )

        return self.__parent__._cast(_7128.AdvancedTimeSteppingAnalysisForModulation)

    @property
    def advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7396.AdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7396,
        )

        return self.__parent__._cast(_7396.AdvancedSystemDeflection)

    @property
    def advanced_system_deflection_sub_analysis(
        self: "CastSelf",
    ) -> "_7398.AdvancedSystemDeflectionSubAnalysis":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7398,
        )

        return self.__parent__._cast(_7398.AdvancedSystemDeflectionSubAnalysis)

    @property
    def compound_analysis_case(self: "CastSelf") -> "_7879.CompoundAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7879,
        )

        return self.__parent__._cast(_7879.CompoundAnalysisCase)

    @property
    def fe_analysis(self: "CastSelf") -> "_7886.FEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7886,
        )

        return self.__parent__._cast(_7886.FEAnalysis)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "StaticLoadAnalysisCase":
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
class StaticLoadAnalysisCase(_7877.AnalysisCase):
    """StaticLoadAnalysisCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATIC_LOAD_ANALYSIS_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def load_case(self: "Self") -> "_7674.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StaticLoadAnalysisCase":
        """Cast to another type.

        Returns:
            _Cast_StaticLoadAnalysisCase
        """
        return _Cast_StaticLoadAnalysisCase(self)
