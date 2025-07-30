"""SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
    _3889,
)

_SPECIALISED_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound",
    "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3857,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
        _3895,
        _3899,
        _3902,
        _3907,
        _3909,
        _3910,
        _3915,
        _3920,
        _3923,
        _3926,
        _3930,
        _3932,
        _3938,
        _3944,
        _3946,
        _3949,
        _3953,
        _3957,
        _3960,
        _3963,
        _3966,
        _3970,
        _3971,
        _3975,
        _3982,
        _3992,
        _3993,
        _3998,
        _4001,
        _4004,
        _4008,
        _4016,
        _4019,
    )

    Self = TypeVar(
        "Self",
        bound="SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed"

    @property
    def abstract_assembly_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3889.AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3889.AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3970.PartCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3970,
        )

        return self.__parent__._cast(
            _3970.PartCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7888.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7888,
        )

        return self.__parent__._cast(_7888.PartCompoundAnalysis)

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
    def agma_gleason_conical_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3895.AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3895,
        )

        return self.__parent__._cast(
            _3895.AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def belt_drive_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3899.BeltDriveCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3899,
        )

        return self.__parent__._cast(
            _3899.BeltDriveCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3902.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3902,
        )

        return self.__parent__._cast(
            _3902.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3907.BevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3907,
        )

        return self.__parent__._cast(
            _3907.BevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bolted_joint_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3909.BoltedJointCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3909,
        )

        return self.__parent__._cast(
            _3909.BoltedJointCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def clutch_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3910.ClutchCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3910,
        )

        return self.__parent__._cast(
            _3910.ClutchCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_coupling_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3915.ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3915,
        )

        return self.__parent__._cast(
            _3915.ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3920.ConceptGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3920,
        )

        return self.__parent__._cast(
            _3920.ConceptGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def conical_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3923.ConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3923,
        )

        return self.__parent__._cast(
            _3923.ConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3926.CouplingCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3926,
        )

        return self.__parent__._cast(
            _3926.CouplingCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cvt_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3930.CVTCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3930,
        )

        return self.__parent__._cast(
            _3930.CVTCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cycloidal_assembly_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3932.CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3932,
        )

        return self.__parent__._cast(
            _3932.CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3938.CylindricalGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3938,
        )

        return self.__parent__._cast(
            _3938.CylindricalGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def face_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3944.FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3944,
        )

        return self.__parent__._cast(
            _3944.FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def flexible_pin_assembly_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3946.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3946,
        )

        return self.__parent__._cast(
            _3946.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3949.GearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3949,
        )

        return self.__parent__._cast(
            _3949.GearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def hypoid_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3953.HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3953,
        )

        return self.__parent__._cast(
            _3953.HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3957.KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3957,
        )

        return self.__parent__._cast(
            _3957.KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3960.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3960,
        )

        return self.__parent__._cast(
            _3960.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3963.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3963,
        )

        return self.__parent__._cast(
            _3963.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def microphone_array_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3966.MicrophoneArrayCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3966,
        )

        return self.__parent__._cast(
            _3966.MicrophoneArrayCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_to_part_shear_coupling_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3971.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3971,
        )

        return self.__parent__._cast(
            _3971.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def planetary_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3975.PlanetaryGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3975,
        )

        return self.__parent__._cast(
            _3975.PlanetaryGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def rolling_ring_assembly_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3982.RollingRingAssemblyCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3982,
        )

        return self.__parent__._cast(
            _3982.RollingRingAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spiral_bevel_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3992.SpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3992,
        )

        return self.__parent__._cast(
            _3992.SpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spring_damper_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3993.SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3993,
        )

        return self.__parent__._cast(
            _3993.SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_diff_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3998.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3998,
        )

        return self.__parent__._cast(
            _3998.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_4001.StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _4001,
        )

        return self.__parent__._cast(
            _4001.StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def synchroniser_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_4004.SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _4004,
        )

        return self.__parent__._cast(
            _4004.SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_4008.TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _4008,
        )

        return self.__parent__._cast(
            _4008.TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def worm_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_4016.WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _4016,
        )

        return self.__parent__._cast(
            _4016.WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def zerol_bevel_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_4019.ZerolBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _4019,
        )

        return self.__parent__._cast(
            _4019.ZerolBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def specialised_assembly_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed":
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
class SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed(
    _3889.AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
):
    """SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _SPECIALISED_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_3857.SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3857.SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed(
            self
        )
