"""ConicalGearCompoundCriticalSpeedAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _7051,
)

_CONICAL_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "ConicalGearCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6891,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6997,
        _7004,
        _7007,
        _7008,
        _7009,
        _7018,
        _7055,
        _7059,
        _7062,
        _7065,
        _7072,
        _7074,
        _7094,
        _7100,
        _7103,
        _7106,
        _7107,
        _7121,
    )

    Self = TypeVar("Self", bound="ConicalGearCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearCompoundCriticalSpeedAnalysis._Cast_ConicalGearCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearCompoundCriticalSpeedAnalysis:
    """Special nested class for casting ConicalGearCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "ConicalGearCompoundCriticalSpeedAnalysis"

    @property
    def gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7051.GearCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(_7051.GearCompoundCriticalSpeedAnalysis)

    @property
    def mountable_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7072.MountableComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7072,
        )

        return self.__parent__._cast(
            _7072.MountableComponentCompoundCriticalSpeedAnalysis
        )

    @property
    def component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7018.ComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7018,
        )

        return self.__parent__._cast(_7018.ComponentCompoundCriticalSpeedAnalysis)

    @property
    def part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7074.PartCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7074,
        )

        return self.__parent__._cast(_7074.PartCompoundCriticalSpeedAnalysis)

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
    def agma_gleason_conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6997.AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6997,
        )

        return self.__parent__._cast(
            _6997.AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7004.BevelDifferentialGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7004,
        )

        return self.__parent__._cast(
            _7004.BevelDifferentialGearCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_planet_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7007.BevelDifferentialPlanetGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7007,
        )

        return self.__parent__._cast(
            _7007.BevelDifferentialPlanetGearCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7008.BevelDifferentialSunGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7008,
        )

        return self.__parent__._cast(
            _7008.BevelDifferentialSunGearCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7009.BevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7009,
        )

        return self.__parent__._cast(_7009.BevelGearCompoundCriticalSpeedAnalysis)

    @property
    def hypoid_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7055.HypoidGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7055,
        )

        return self.__parent__._cast(_7055.HypoidGearCompoundCriticalSpeedAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7059.KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7059,
        )

        return self.__parent__._cast(
            _7059.KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7062.KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7062,
        )

        return self.__parent__._cast(
            _7062.KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7065.KlingelnbergCycloPalloidSpiralBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7065,
        )

        return self.__parent__._cast(
            _7065.KlingelnbergCycloPalloidSpiralBevelGearCompoundCriticalSpeedAnalysis
        )

    @property
    def spiral_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7094.SpiralBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7094,
        )

        return self.__parent__._cast(_7094.SpiralBevelGearCompoundCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7100.StraightBevelDiffGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7100,
        )

        return self.__parent__._cast(
            _7100.StraightBevelDiffGearCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7103.StraightBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7103,
        )

        return self.__parent__._cast(
            _7103.StraightBevelGearCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_planet_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7106.StraightBevelPlanetGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7106,
        )

        return self.__parent__._cast(
            _7106.StraightBevelPlanetGearCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7107.StraightBevelSunGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7107,
        )

        return self.__parent__._cast(
            _7107.StraightBevelSunGearCompoundCriticalSpeedAnalysis
        )

    @property
    def zerol_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7121.ZerolBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7121,
        )

        return self.__parent__._cast(_7121.ZerolBevelGearCompoundCriticalSpeedAnalysis)

    @property
    def conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "ConicalGearCompoundCriticalSpeedAnalysis":
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
class ConicalGearCompoundCriticalSpeedAnalysis(_7051.GearCompoundCriticalSpeedAnalysis):
    """ConicalGearCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def planetaries(self: "Self") -> "List[ConicalGearCompoundCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.compound.ConicalGearCompoundCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6891.ConicalGearCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.ConicalGearCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6891.ConicalGearCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.ConicalGearCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearCompoundCriticalSpeedAnalysis
        """
        return _Cast_ConicalGearCompoundCriticalSpeedAnalysis(self)
