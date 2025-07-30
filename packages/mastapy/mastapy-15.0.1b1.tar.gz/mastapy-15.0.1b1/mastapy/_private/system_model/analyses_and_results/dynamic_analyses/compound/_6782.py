"""GearSetCompoundDynamicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6822,
)

_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "GearSetCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6651,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6722,
        _6728,
        _6735,
        _6740,
        _6753,
        _6756,
        _6771,
        _6777,
        _6786,
        _6790,
        _6793,
        _6796,
        _6803,
        _6808,
        _6825,
        _6831,
        _6834,
        _6849,
        _6852,
    )

    Self = TypeVar("Self", bound="GearSetCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetCompoundDynamicAnalysis._Cast_GearSetCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetCompoundDynamicAnalysis:
    """Special nested class for casting GearSetCompoundDynamicAnalysis to subclasses."""

    __parent__: "GearSetCompoundDynamicAnalysis"

    @property
    def specialised_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6822.SpecialisedAssemblyCompoundDynamicAnalysis":
        return self.__parent__._cast(_6822.SpecialisedAssemblyCompoundDynamicAnalysis)

    @property
    def abstract_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6722.AbstractAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6722,
        )

        return self.__parent__._cast(_6722.AbstractAssemblyCompoundDynamicAnalysis)

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6803.PartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6803,
        )

        return self.__parent__._cast(_6803.PartCompoundDynamicAnalysis)

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
    def agma_gleason_conical_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6728.AGMAGleasonConicalGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6728,
        )

        return self.__parent__._cast(
            _6728.AGMAGleasonConicalGearSetCompoundDynamicAnalysis
        )

    @property
    def bevel_differential_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6735.BevelDifferentialGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6735,
        )

        return self.__parent__._cast(
            _6735.BevelDifferentialGearSetCompoundDynamicAnalysis
        )

    @property
    def bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6740.BevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6740,
        )

        return self.__parent__._cast(_6740.BevelGearSetCompoundDynamicAnalysis)

    @property
    def concept_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6753.ConceptGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6753,
        )

        return self.__parent__._cast(_6753.ConceptGearSetCompoundDynamicAnalysis)

    @property
    def conical_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6756.ConicalGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6756,
        )

        return self.__parent__._cast(_6756.ConicalGearSetCompoundDynamicAnalysis)

    @property
    def cylindrical_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6771.CylindricalGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6771,
        )

        return self.__parent__._cast(_6771.CylindricalGearSetCompoundDynamicAnalysis)

    @property
    def face_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6777.FaceGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6777,
        )

        return self.__parent__._cast(_6777.FaceGearSetCompoundDynamicAnalysis)

    @property
    def hypoid_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6786.HypoidGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6786,
        )

        return self.__parent__._cast(_6786.HypoidGearSetCompoundDynamicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6790.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6790,
        )

        return self.__parent__._cast(
            _6790.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6793.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6793,
        )

        return self.__parent__._cast(
            _6793.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6796.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6796,
        )

        return self.__parent__._cast(
            _6796.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis
        )

    @property
    def planetary_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6808.PlanetaryGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6808,
        )

        return self.__parent__._cast(_6808.PlanetaryGearSetCompoundDynamicAnalysis)

    @property
    def spiral_bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6825.SpiralBevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6825,
        )

        return self.__parent__._cast(_6825.SpiralBevelGearSetCompoundDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6831.StraightBevelDiffGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6831,
        )

        return self.__parent__._cast(
            _6831.StraightBevelDiffGearSetCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6834.StraightBevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6834,
        )

        return self.__parent__._cast(_6834.StraightBevelGearSetCompoundDynamicAnalysis)

    @property
    def worm_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6849.WormGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6849,
        )

        return self.__parent__._cast(_6849.WormGearSetCompoundDynamicAnalysis)

    @property
    def zerol_bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6852.ZerolBevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6852,
        )

        return self.__parent__._cast(_6852.ZerolBevelGearSetCompoundDynamicAnalysis)

    @property
    def gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "GearSetCompoundDynamicAnalysis":
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
class GearSetCompoundDynamicAnalysis(_6822.SpecialisedAssemblyCompoundDynamicAnalysis):
    """GearSetCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases(self: "Self") -> "List[_6651.GearSetDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.GearSetDynamicAnalysis]

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
    ) -> "List[_6651.GearSetDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.GearSetDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_GearSetCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearSetCompoundDynamicAnalysis
        """
        return _Cast_GearSetCompoundDynamicAnalysis(self)
