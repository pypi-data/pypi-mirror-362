"""AbstractAssemblyCompoundModalAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _5082,
)

_ABSTRACT_ASSEMBLY_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "AbstractAssemblyCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4842
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _5007,
        _5008,
        _5011,
        _5014,
        _5019,
        _5021,
        _5022,
        _5027,
        _5032,
        _5035,
        _5038,
        _5042,
        _5044,
        _5050,
        _5056,
        _5058,
        _5061,
        _5065,
        _5069,
        _5072,
        _5075,
        _5078,
        _5083,
        _5087,
        _5094,
        _5097,
        _5101,
        _5104,
        _5105,
        _5110,
        _5113,
        _5116,
        _5120,
        _5128,
        _5131,
    )

    Self = TypeVar("Self", bound="AbstractAssemblyCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractAssemblyCompoundModalAnalysis._Cast_AbstractAssemblyCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyCompoundModalAnalysis:
    """Special nested class for casting AbstractAssemblyCompoundModalAnalysis to subclasses."""

    __parent__: "AbstractAssemblyCompoundModalAnalysis"

    @property
    def part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5082.PartCompoundModalAnalysis":
        return self.__parent__._cast(_5082.PartCompoundModalAnalysis)

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
    def agma_gleason_conical_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5007.AGMAGleasonConicalGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5007,
        )

        return self.__parent__._cast(
            _5007.AGMAGleasonConicalGearSetCompoundModalAnalysis
        )

    @property
    def assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5008.AssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5008,
        )

        return self.__parent__._cast(_5008.AssemblyCompoundModalAnalysis)

    @property
    def belt_drive_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5011.BeltDriveCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5011,
        )

        return self.__parent__._cast(_5011.BeltDriveCompoundModalAnalysis)

    @property
    def bevel_differential_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5014.BevelDifferentialGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5014,
        )

        return self.__parent__._cast(
            _5014.BevelDifferentialGearSetCompoundModalAnalysis
        )

    @property
    def bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5019.BevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5019,
        )

        return self.__parent__._cast(_5019.BevelGearSetCompoundModalAnalysis)

    @property
    def bolted_joint_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5021.BoltedJointCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5021,
        )

        return self.__parent__._cast(_5021.BoltedJointCompoundModalAnalysis)

    @property
    def clutch_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5022.ClutchCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5022,
        )

        return self.__parent__._cast(_5022.ClutchCompoundModalAnalysis)

    @property
    def concept_coupling_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5027.ConceptCouplingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5027,
        )

        return self.__parent__._cast(_5027.ConceptCouplingCompoundModalAnalysis)

    @property
    def concept_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5032.ConceptGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5032,
        )

        return self.__parent__._cast(_5032.ConceptGearSetCompoundModalAnalysis)

    @property
    def conical_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5035.ConicalGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5035,
        )

        return self.__parent__._cast(_5035.ConicalGearSetCompoundModalAnalysis)

    @property
    def coupling_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5038.CouplingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5038,
        )

        return self.__parent__._cast(_5038.CouplingCompoundModalAnalysis)

    @property
    def cvt_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5042.CVTCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5042,
        )

        return self.__parent__._cast(_5042.CVTCompoundModalAnalysis)

    @property
    def cycloidal_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5044.CycloidalAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5044,
        )

        return self.__parent__._cast(_5044.CycloidalAssemblyCompoundModalAnalysis)

    @property
    def cylindrical_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5050.CylindricalGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5050,
        )

        return self.__parent__._cast(_5050.CylindricalGearSetCompoundModalAnalysis)

    @property
    def face_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5056.FaceGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5056,
        )

        return self.__parent__._cast(_5056.FaceGearSetCompoundModalAnalysis)

    @property
    def flexible_pin_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5058.FlexiblePinAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5058,
        )

        return self.__parent__._cast(_5058.FlexiblePinAssemblyCompoundModalAnalysis)

    @property
    def gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5061.GearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5061,
        )

        return self.__parent__._cast(_5061.GearSetCompoundModalAnalysis)

    @property
    def hypoid_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5065.HypoidGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5065,
        )

        return self.__parent__._cast(_5065.HypoidGearSetCompoundModalAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5069.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5069,
        )

        return self.__parent__._cast(
            _5069.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5072.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5072,
        )

        return self.__parent__._cast(
            _5072.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5075.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5075,
        )

        return self.__parent__._cast(
            _5075.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis
        )

    @property
    def microphone_array_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5078.MicrophoneArrayCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5078,
        )

        return self.__parent__._cast(_5078.MicrophoneArrayCompoundModalAnalysis)

    @property
    def part_to_part_shear_coupling_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5083.PartToPartShearCouplingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5083,
        )

        return self.__parent__._cast(_5083.PartToPartShearCouplingCompoundModalAnalysis)

    @property
    def planetary_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5087.PlanetaryGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5087,
        )

        return self.__parent__._cast(_5087.PlanetaryGearSetCompoundModalAnalysis)

    @property
    def rolling_ring_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5094.RollingRingAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5094,
        )

        return self.__parent__._cast(_5094.RollingRingAssemblyCompoundModalAnalysis)

    @property
    def root_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5097.RootAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5097,
        )

        return self.__parent__._cast(_5097.RootAssemblyCompoundModalAnalysis)

    @property
    def specialised_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5101.SpecialisedAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5101,
        )

        return self.__parent__._cast(_5101.SpecialisedAssemblyCompoundModalAnalysis)

    @property
    def spiral_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5104.SpiralBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5104,
        )

        return self.__parent__._cast(_5104.SpiralBevelGearSetCompoundModalAnalysis)

    @property
    def spring_damper_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5105.SpringDamperCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5105,
        )

        return self.__parent__._cast(_5105.SpringDamperCompoundModalAnalysis)

    @property
    def straight_bevel_diff_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5110.StraightBevelDiffGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5110,
        )

        return self.__parent__._cast(
            _5110.StraightBevelDiffGearSetCompoundModalAnalysis
        )

    @property
    def straight_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5113.StraightBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5113,
        )

        return self.__parent__._cast(_5113.StraightBevelGearSetCompoundModalAnalysis)

    @property
    def synchroniser_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5116.SynchroniserCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5116,
        )

        return self.__parent__._cast(_5116.SynchroniserCompoundModalAnalysis)

    @property
    def torque_converter_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5120.TorqueConverterCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5120,
        )

        return self.__parent__._cast(_5120.TorqueConverterCompoundModalAnalysis)

    @property
    def worm_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5128.WormGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5128,
        )

        return self.__parent__._cast(_5128.WormGearSetCompoundModalAnalysis)

    @property
    def zerol_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5131.ZerolBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5131,
        )

        return self.__parent__._cast(_5131.ZerolBevelGearSetCompoundModalAnalysis)

    @property
    def abstract_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "AbstractAssemblyCompoundModalAnalysis":
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
class AbstractAssemblyCompoundModalAnalysis(_5082.PartCompoundModalAnalysis):
    """AbstractAssemblyCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_COMPOUND_MODAL_ANALYSIS

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
    ) -> "List[_4842.AbstractAssemblyModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.AbstractAssemblyModalAnalysis]

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
    ) -> "List[_4842.AbstractAssemblyModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.AbstractAssemblyModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyCompoundModalAnalysis
        """
        return _Cast_AbstractAssemblyCompoundModalAnalysis(self)
