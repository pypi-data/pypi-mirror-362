"""GearSetCompoundModalAnalysis"""

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
    _5101,
)

_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "GearSetCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4907
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _5001,
        _5007,
        _5014,
        _5019,
        _5032,
        _5035,
        _5050,
        _5056,
        _5065,
        _5069,
        _5072,
        _5075,
        _5082,
        _5087,
        _5104,
        _5110,
        _5113,
        _5128,
        _5131,
    )

    Self = TypeVar("Self", bound="GearSetCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetCompoundModalAnalysis._Cast_GearSetCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetCompoundModalAnalysis:
    """Special nested class for casting GearSetCompoundModalAnalysis to subclasses."""

    __parent__: "GearSetCompoundModalAnalysis"

    @property
    def specialised_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5101.SpecialisedAssemblyCompoundModalAnalysis":
        return self.__parent__._cast(_5101.SpecialisedAssemblyCompoundModalAnalysis)

    @property
    def abstract_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5001.AbstractAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5001,
        )

        return self.__parent__._cast(_5001.AbstractAssemblyCompoundModalAnalysis)

    @property
    def part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5082.PartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5082,
        )

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
    def planetary_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5087.PlanetaryGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5087,
        )

        return self.__parent__._cast(_5087.PlanetaryGearSetCompoundModalAnalysis)

    @property
    def spiral_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5104.SpiralBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5104,
        )

        return self.__parent__._cast(_5104.SpiralBevelGearSetCompoundModalAnalysis)

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
    def gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "GearSetCompoundModalAnalysis":
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
class GearSetCompoundModalAnalysis(_5101.SpecialisedAssemblyCompoundModalAnalysis):
    """GearSetCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases(self: "Self") -> "List[_4907.GearSetModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.GearSetModalAnalysis]

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
    ) -> "List[_4907.GearSetModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.GearSetModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_GearSetCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearSetCompoundModalAnalysis
        """
        return _Cast_GearSetCompoundModalAnalysis(self)
