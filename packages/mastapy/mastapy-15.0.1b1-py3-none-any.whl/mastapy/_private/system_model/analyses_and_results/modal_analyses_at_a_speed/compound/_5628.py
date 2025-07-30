"""SpecialisedAssemblyCompoundModalAnalysisAtASpeed"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5528,
)

_SPECIALISED_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
    "SpecialisedAssemblyCompoundModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5497,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5534,
        _5538,
        _5541,
        _5546,
        _5548,
        _5549,
        _5554,
        _5559,
        _5562,
        _5565,
        _5569,
        _5571,
        _5577,
        _5583,
        _5585,
        _5588,
        _5592,
        _5596,
        _5599,
        _5602,
        _5605,
        _5609,
        _5610,
        _5614,
        _5621,
        _5631,
        _5632,
        _5637,
        _5640,
        _5643,
        _5647,
        _5655,
        _5658,
    )

    Self = TypeVar("Self", bound="SpecialisedAssemblyCompoundModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyCompoundModalAnalysisAtASpeed._Cast_SpecialisedAssemblyCompoundModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCompoundModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyCompoundModalAnalysisAtASpeed:
    """Special nested class for casting SpecialisedAssemblyCompoundModalAnalysisAtASpeed to subclasses."""

    __parent__: "SpecialisedAssemblyCompoundModalAnalysisAtASpeed"

    @property
    def abstract_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5528.AbstractAssemblyCompoundModalAnalysisAtASpeed":
        return self.__parent__._cast(
            _5528.AbstractAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5609.PartCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5609,
        )

        return self.__parent__._cast(_5609.PartCompoundModalAnalysisAtASpeed)

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
    def agma_gleason_conical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5534.AGMAGleasonConicalGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5534,
        )

        return self.__parent__._cast(
            _5534.AGMAGleasonConicalGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def belt_drive_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5538.BeltDriveCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5538,
        )

        return self.__parent__._cast(_5538.BeltDriveCompoundModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5541.BevelDifferentialGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5541,
        )

        return self.__parent__._cast(
            _5541.BevelDifferentialGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5546.BevelGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5546,
        )

        return self.__parent__._cast(_5546.BevelGearSetCompoundModalAnalysisAtASpeed)

    @property
    def bolted_joint_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5548.BoltedJointCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5548,
        )

        return self.__parent__._cast(_5548.BoltedJointCompoundModalAnalysisAtASpeed)

    @property
    def clutch_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5549.ClutchCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5549,
        )

        return self.__parent__._cast(_5549.ClutchCompoundModalAnalysisAtASpeed)

    @property
    def concept_coupling_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5554.ConceptCouplingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5554,
        )

        return self.__parent__._cast(_5554.ConceptCouplingCompoundModalAnalysisAtASpeed)

    @property
    def concept_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5559.ConceptGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5559,
        )

        return self.__parent__._cast(_5559.ConceptGearSetCompoundModalAnalysisAtASpeed)

    @property
    def conical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5562.ConicalGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5562,
        )

        return self.__parent__._cast(_5562.ConicalGearSetCompoundModalAnalysisAtASpeed)

    @property
    def coupling_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5565.CouplingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5565,
        )

        return self.__parent__._cast(_5565.CouplingCompoundModalAnalysisAtASpeed)

    @property
    def cvt_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5569.CVTCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5569,
        )

        return self.__parent__._cast(_5569.CVTCompoundModalAnalysisAtASpeed)

    @property
    def cycloidal_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5571.CycloidalAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5571,
        )

        return self.__parent__._cast(
            _5571.CycloidalAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def cylindrical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5577.CylindricalGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5577,
        )

        return self.__parent__._cast(
            _5577.CylindricalGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def face_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5583.FaceGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5583,
        )

        return self.__parent__._cast(_5583.FaceGearSetCompoundModalAnalysisAtASpeed)

    @property
    def flexible_pin_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5585.FlexiblePinAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5585,
        )

        return self.__parent__._cast(
            _5585.FlexiblePinAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5588.GearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5588,
        )

        return self.__parent__._cast(_5588.GearSetCompoundModalAnalysisAtASpeed)

    @property
    def hypoid_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5592.HypoidGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5592,
        )

        return self.__parent__._cast(_5592.HypoidGearSetCompoundModalAnalysisAtASpeed)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5596.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5596,
        )

        return self.__parent__._cast(
            _5596.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5599.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5599,
        )

        return self.__parent__._cast(
            _5599.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_5602.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5602,
        )

        return self.__parent__._cast(
            _5602.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def microphone_array_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5605.MicrophoneArrayCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5605,
        )

        return self.__parent__._cast(_5605.MicrophoneArrayCompoundModalAnalysisAtASpeed)

    @property
    def part_to_part_shear_coupling_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5610.PartToPartShearCouplingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5610,
        )

        return self.__parent__._cast(
            _5610.PartToPartShearCouplingCompoundModalAnalysisAtASpeed
        )

    @property
    def planetary_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5614.PlanetaryGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5614,
        )

        return self.__parent__._cast(
            _5614.PlanetaryGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def rolling_ring_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5621.RollingRingAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5621,
        )

        return self.__parent__._cast(
            _5621.RollingRingAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def spiral_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5631.SpiralBevelGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5631,
        )

        return self.__parent__._cast(
            _5631.SpiralBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def spring_damper_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5632.SpringDamperCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5632,
        )

        return self.__parent__._cast(_5632.SpringDamperCompoundModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5637.StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5637,
        )

        return self.__parent__._cast(
            _5637.StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5640.StraightBevelGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5640,
        )

        return self.__parent__._cast(
            _5640.StraightBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def synchroniser_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5643.SynchroniserCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5643,
        )

        return self.__parent__._cast(_5643.SynchroniserCompoundModalAnalysisAtASpeed)

    @property
    def torque_converter_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5647.TorqueConverterCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5647,
        )

        return self.__parent__._cast(_5647.TorqueConverterCompoundModalAnalysisAtASpeed)

    @property
    def worm_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5655.WormGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5655,
        )

        return self.__parent__._cast(_5655.WormGearSetCompoundModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5658.ZerolBevelGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5658,
        )

        return self.__parent__._cast(
            _5658.ZerolBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def specialised_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyCompoundModalAnalysisAtASpeed":
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
class SpecialisedAssemblyCompoundModalAnalysisAtASpeed(
    _5528.AbstractAssemblyCompoundModalAnalysisAtASpeed
):
    """SpecialisedAssemblyCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

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
    ) -> "List[_5497.SpecialisedAssemblyModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.SpecialisedAssemblyModalAnalysisAtASpeed]

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
    ) -> "List[_5497.SpecialisedAssemblyModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.SpecialisedAssemblyModalAnalysisAtASpeed]

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
    ) -> "_Cast_SpecialisedAssemblyCompoundModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyCompoundModalAnalysisAtASpeed
        """
        return _Cast_SpecialisedAssemblyCompoundModalAnalysisAtASpeed(self)
