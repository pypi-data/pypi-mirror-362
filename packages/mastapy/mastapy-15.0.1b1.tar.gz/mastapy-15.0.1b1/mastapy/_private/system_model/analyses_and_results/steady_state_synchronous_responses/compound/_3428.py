"""InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3398,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3294,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3368,
        _3372,
        _3375,
        _3380,
        _3385,
        _3390,
        _3393,
        _3396,
        _3401,
        _3403,
        _3411,
        _3417,
        _3422,
        _3426,
        _3430,
        _3433,
        _3436,
        _3446,
        _3455,
        _3458,
        _3465,
        _3468,
        _3471,
        _3474,
        _3483,
        _3489,
        _3492,
    )

    Self = TypeVar(
        "Self",
        bound="InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse._Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse:
    """Special nested class for casting InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse to subclasses."""

    __parent__: (
        "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse"
    )

    @property
    def connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3398.ConnectionCompoundSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3398.ConnectionCompoundSteadyStateSynchronousResponse
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
    def agma_gleason_conical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3368.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3368,
        )

        return self.__parent__._cast(
            _3368.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def belt_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3372.BeltConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3372,
        )

        return self.__parent__._cast(
            _3372.BeltConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3375.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3375,
        )

        return self.__parent__._cast(
            _3375.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3380.BevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3380,
        )

        return self.__parent__._cast(
            _3380.BevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def clutch_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3385.ClutchConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3385,
        )

        return self.__parent__._cast(
            _3385.ClutchConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def concept_coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3390.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3390,
        )

        return self.__parent__._cast(
            _3390.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def concept_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3393.ConceptGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3393,
        )

        return self.__parent__._cast(
            _3393.ConceptGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3396.ConicalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3396,
        )

        return self.__parent__._cast(
            _3396.ConicalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3401.CouplingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3401,
        )

        return self.__parent__._cast(
            _3401.CouplingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def cvt_belt_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3403.CVTBeltConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3403,
        )

        return self.__parent__._cast(
            _3403.CVTBeltConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3411.CylindricalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3411,
        )

        return self.__parent__._cast(
            _3411.CylindricalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def face_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3417.FaceGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3417,
        )

        return self.__parent__._cast(
            _3417.FaceGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3422.GearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3422,
        )

        return self.__parent__._cast(
            _3422.GearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def hypoid_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3426.HypoidGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3426,
        )

        return self.__parent__._cast(
            _3426.HypoidGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3430.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3430,
        )

        return self.__parent__._cast(
            _3430.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3433.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3433,
        )

        return self.__parent__._cast(
            _3433.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3436.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3436,
        )

        return self.__parent__._cast(
            _3436.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def part_to_part_shear_coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> (
        "_3446.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3446,
        )

        return self.__parent__._cast(
            _3446.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def ring_pins_to_disc_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3455.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3455,
        )

        return self.__parent__._cast(
            _3455.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def rolling_ring_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3458.RollingRingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3458,
        )

        return self.__parent__._cast(
            _3458.RollingRingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3465.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3465,
        )

        return self.__parent__._cast(
            _3465.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def spring_damper_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3468.SpringDamperConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3468,
        )

        return self.__parent__._cast(
            _3468.SpringDamperConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3471.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3471,
        )

        return self.__parent__._cast(
            _3471.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3474.StraightBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3474,
        )

        return self.__parent__._cast(
            _3474.StraightBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3483.TorqueConverterConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3483,
        )

        return self.__parent__._cast(
            _3483.TorqueConverterConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def worm_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3489.WormGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3489,
        )

        return self.__parent__._cast(
            _3489.WormGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def zerol_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3492.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3492,
        )

        return self.__parent__._cast(
            _3492.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def inter_mountable_component_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse":
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
class InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse(
    _3398.ConnectionCompoundSteadyStateSynchronousResponse
):
    """InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_3294.InterMountableComponentConnectionSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.InterMountableComponentConnectionSteadyStateSynchronousResponse]

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
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3294.InterMountableComponentConnectionSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.InterMountableComponentConnectionSteadyStateSynchronousResponse]

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
    def cast_to(
        self: "Self",
    ) -> (
        "_Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse"
    ):
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse
        """
        return _Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse(
            self
        )
