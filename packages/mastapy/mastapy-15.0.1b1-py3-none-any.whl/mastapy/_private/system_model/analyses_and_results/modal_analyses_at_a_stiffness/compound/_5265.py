"""AbstractAssemblyCompoundModalAnalysisAtAStiffness"""

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
    _5346,
)

_ABSTRACT_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "AbstractAssemblyCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5132,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5271,
        _5272,
        _5275,
        _5278,
        _5283,
        _5285,
        _5286,
        _5291,
        _5296,
        _5299,
        _5302,
        _5306,
        _5308,
        _5314,
        _5320,
        _5322,
        _5325,
        _5329,
        _5333,
        _5336,
        _5339,
        _5342,
        _5347,
        _5351,
        _5358,
        _5361,
        _5365,
        _5368,
        _5369,
        _5374,
        _5377,
        _5380,
        _5384,
        _5392,
        _5395,
    )

    Self = TypeVar("Self", bound="AbstractAssemblyCompoundModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractAssemblyCompoundModalAnalysisAtAStiffness._Cast_AbstractAssemblyCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting AbstractAssemblyCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "AbstractAssemblyCompoundModalAnalysisAtAStiffness"

    @property
    def part_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5346.PartCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(_5346.PartCompoundModalAnalysisAtAStiffness)

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
    def agma_gleason_conical_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5271.AGMAGleasonConicalGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5271,
        )

        return self.__parent__._cast(
            _5271.AGMAGleasonConicalGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5272.AssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5272,
        )

        return self.__parent__._cast(_5272.AssemblyCompoundModalAnalysisAtAStiffness)

    @property
    def belt_drive_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5275.BeltDriveCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5275,
        )

        return self.__parent__._cast(_5275.BeltDriveCompoundModalAnalysisAtAStiffness)

    @property
    def bevel_differential_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5278.BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5278,
        )

        return self.__parent__._cast(
            _5278.BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5283.BevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5283,
        )

        return self.__parent__._cast(
            _5283.BevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def bolted_joint_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5285.BoltedJointCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5285,
        )

        return self.__parent__._cast(_5285.BoltedJointCompoundModalAnalysisAtAStiffness)

    @property
    def clutch_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5286.ClutchCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5286,
        )

        return self.__parent__._cast(_5286.ClutchCompoundModalAnalysisAtAStiffness)

    @property
    def concept_coupling_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5291.ConceptCouplingCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5291,
        )

        return self.__parent__._cast(
            _5291.ConceptCouplingCompoundModalAnalysisAtAStiffness
        )

    @property
    def concept_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5296.ConceptGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5296,
        )

        return self.__parent__._cast(
            _5296.ConceptGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def conical_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5299.ConicalGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5299,
        )

        return self.__parent__._cast(
            _5299.ConicalGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def coupling_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5302.CouplingCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5302,
        )

        return self.__parent__._cast(_5302.CouplingCompoundModalAnalysisAtAStiffness)

    @property
    def cvt_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5306.CVTCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5306,
        )

        return self.__parent__._cast(_5306.CVTCompoundModalAnalysisAtAStiffness)

    @property
    def cycloidal_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5308.CycloidalAssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5308,
        )

        return self.__parent__._cast(
            _5308.CycloidalAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def cylindrical_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5314.CylindricalGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5314,
        )

        return self.__parent__._cast(
            _5314.CylindricalGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def face_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5320.FaceGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5320,
        )

        return self.__parent__._cast(_5320.FaceGearSetCompoundModalAnalysisAtAStiffness)

    @property
    def flexible_pin_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5322.FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5322,
        )

        return self.__parent__._cast(
            _5322.FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5325.GearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5325,
        )

        return self.__parent__._cast(_5325.GearSetCompoundModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5329.HypoidGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5329,
        )

        return self.__parent__._cast(
            _5329.HypoidGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> (
        "_5333.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtAStiffness"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5333,
        )

        return self.__parent__._cast(
            _5333.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5336.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5336,
        )

        return self.__parent__._cast(
            _5336.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5339.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5339,
        )

        return self.__parent__._cast(
            _5339.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def microphone_array_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5342.MicrophoneArrayCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5342,
        )

        return self.__parent__._cast(
            _5342.MicrophoneArrayCompoundModalAnalysisAtAStiffness
        )

    @property
    def part_to_part_shear_coupling_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5347.PartToPartShearCouplingCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5347,
        )

        return self.__parent__._cast(
            _5347.PartToPartShearCouplingCompoundModalAnalysisAtAStiffness
        )

    @property
    def planetary_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5351.PlanetaryGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5351,
        )

        return self.__parent__._cast(
            _5351.PlanetaryGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def rolling_ring_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5358.RollingRingAssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5358,
        )

        return self.__parent__._cast(
            _5358.RollingRingAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def root_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5361.RootAssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5361,
        )

        return self.__parent__._cast(
            _5361.RootAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def specialised_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5365.SpecialisedAssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5365,
        )

        return self.__parent__._cast(
            _5365.SpecialisedAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def spiral_bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5368.SpiralBevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5368,
        )

        return self.__parent__._cast(
            _5368.SpiralBevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def spring_damper_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5369.SpringDamperCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5369,
        )

        return self.__parent__._cast(
            _5369.SpringDamperCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_diff_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5374.StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5374,
        )

        return self.__parent__._cast(
            _5374.StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5377.StraightBevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5377,
        )

        return self.__parent__._cast(
            _5377.StraightBevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def synchroniser_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5380.SynchroniserCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5380,
        )

        return self.__parent__._cast(
            _5380.SynchroniserCompoundModalAnalysisAtAStiffness
        )

    @property
    def torque_converter_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5384.TorqueConverterCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5384,
        )

        return self.__parent__._cast(
            _5384.TorqueConverterCompoundModalAnalysisAtAStiffness
        )

    @property
    def worm_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5392.WormGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5392,
        )

        return self.__parent__._cast(_5392.WormGearSetCompoundModalAnalysisAtAStiffness)

    @property
    def zerol_bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5395.ZerolBevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5395,
        )

        return self.__parent__._cast(
            _5395.ZerolBevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def abstract_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "AbstractAssemblyCompoundModalAnalysisAtAStiffness":
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
class AbstractAssemblyCompoundModalAnalysisAtAStiffness(
    _5346.PartCompoundModalAnalysisAtAStiffness
):
    """AbstractAssemblyCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

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
    ) -> "List[_5132.AbstractAssemblyModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.AbstractAssemblyModalAnalysisAtAStiffness]

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
    ) -> "List[_5132.AbstractAssemblyModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.AbstractAssemblyModalAnalysisAtAStiffness]

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
    ) -> "_Cast_AbstractAssemblyCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyCompoundModalAnalysisAtAStiffness
        """
        return _Cast_AbstractAssemblyCompoundModalAnalysisAtAStiffness(self)
