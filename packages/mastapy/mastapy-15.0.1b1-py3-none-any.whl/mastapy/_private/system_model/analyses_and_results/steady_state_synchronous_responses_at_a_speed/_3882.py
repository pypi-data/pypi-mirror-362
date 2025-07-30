"""VirtualComponentSteadyStateSynchronousResponseAtASpeed"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _3836,
)

_VIRTUAL_COMPONENT_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "VirtualComponentSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3782,
        _3832,
        _3833,
        _3838,
        _3845,
        _3846,
        _3881,
    )
    from mastapy._private.system_model.part_model import _2711

    Self = TypeVar(
        "Self", bound="VirtualComponentSteadyStateSynchronousResponseAtASpeed"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentSteadyStateSynchronousResponseAtASpeed._Cast_VirtualComponentSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting VirtualComponentSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "VirtualComponentSteadyStateSynchronousResponseAtASpeed"

    @property
    def mountable_component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3836.MountableComponentSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3836.MountableComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3782.ComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3782,
        )

        return self.__parent__._cast(
            _3782.ComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3838.PartSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3838,
        )

        return self.__parent__._cast(_3838.PartSteadyStateSynchronousResponseAtASpeed)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7890.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7890,
        )

        return self.__parent__._cast(_7890.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7887.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7887,
        )

        return self.__parent__._cast(_7887.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def mass_disc_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3832.MassDiscSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3832,
        )

        return self.__parent__._cast(
            _3832.MassDiscSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def measurement_component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3833.MeasurementComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3833,
        )

        return self.__parent__._cast(
            _3833.MeasurementComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def point_load_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3845.PointLoadSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3845,
        )

        return self.__parent__._cast(
            _3845.PointLoadSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def power_load_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3846.PowerLoadSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3846,
        )

        return self.__parent__._cast(
            _3846.PowerLoadSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def unbalanced_mass_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3881.UnbalancedMassSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3881,
        )

        return self.__parent__._cast(
            _3881.UnbalancedMassSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def virtual_component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "VirtualComponentSteadyStateSynchronousResponseAtASpeed":
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
class VirtualComponentSteadyStateSynchronousResponseAtASpeed(
    _3836.MountableComponentSteadyStateSynchronousResponseAtASpeed
):
    """VirtualComponentSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _VIRTUAL_COMPONENT_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2711.VirtualComponent":
        """mastapy.system_model.part_model.VirtualComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_VirtualComponentSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_VirtualComponentSteadyStateSynchronousResponseAtASpeed(self)
