"""MountableComponentCompoundCriticalSpeedAnalysis"""

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
    _7018,
)

_MOUNTABLE_COMPONENT_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "MountableComponentCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6941,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6997,
        _7001,
        _7004,
        _7007,
        _7008,
        _7009,
        _7016,
        _7021,
        _7022,
        _7025,
        _7029,
        _7032,
        _7035,
        _7040,
        _7043,
        _7046,
        _7051,
        _7055,
        _7059,
        _7062,
        _7065,
        _7068,
        _7069,
        _7073,
        _7074,
        _7077,
        _7080,
        _7081,
        _7082,
        _7083,
        _7084,
        _7087,
        _7091,
        _7094,
        _7099,
        _7100,
        _7103,
        _7106,
        _7107,
        _7109,
        _7110,
        _7111,
        _7114,
        _7115,
        _7116,
        _7117,
        _7118,
        _7121,
    )

    Self = TypeVar("Self", bound="MountableComponentCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentCompoundCriticalSpeedAnalysis._Cast_MountableComponentCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentCompoundCriticalSpeedAnalysis:
    """Special nested class for casting MountableComponentCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "MountableComponentCompoundCriticalSpeedAnalysis"

    @property
    def component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7018.ComponentCompoundCriticalSpeedAnalysis":
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
    def bearing_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7001.BearingCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7001,
        )

        return self.__parent__._cast(_7001.BearingCompoundCriticalSpeedAnalysis)

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
    def clutch_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7016.ClutchHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7016,
        )

        return self.__parent__._cast(_7016.ClutchHalfCompoundCriticalSpeedAnalysis)

    @property
    def concept_coupling_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7021.ConceptCouplingHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7021,
        )

        return self.__parent__._cast(
            _7021.ConceptCouplingHalfCompoundCriticalSpeedAnalysis
        )

    @property
    def concept_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7022.ConceptGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7022,
        )

        return self.__parent__._cast(_7022.ConceptGearCompoundCriticalSpeedAnalysis)

    @property
    def conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7025.ConicalGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7025,
        )

        return self.__parent__._cast(_7025.ConicalGearCompoundCriticalSpeedAnalysis)

    @property
    def connector_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7029.ConnectorCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7029,
        )

        return self.__parent__._cast(_7029.ConnectorCompoundCriticalSpeedAnalysis)

    @property
    def coupling_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7032.CouplingHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7032,
        )

        return self.__parent__._cast(_7032.CouplingHalfCompoundCriticalSpeedAnalysis)

    @property
    def cvt_pulley_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7035.CVTPulleyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7035,
        )

        return self.__parent__._cast(_7035.CVTPulleyCompoundCriticalSpeedAnalysis)

    @property
    def cylindrical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7040.CylindricalGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7040,
        )

        return self.__parent__._cast(_7040.CylindricalGearCompoundCriticalSpeedAnalysis)

    @property
    def cylindrical_planet_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7043.CylindricalPlanetGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7043,
        )

        return self.__parent__._cast(
            _7043.CylindricalPlanetGearCompoundCriticalSpeedAnalysis
        )

    @property
    def face_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7046.FaceGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7046,
        )

        return self.__parent__._cast(_7046.FaceGearCompoundCriticalSpeedAnalysis)

    @property
    def gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7051.GearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7051,
        )

        return self.__parent__._cast(_7051.GearCompoundCriticalSpeedAnalysis)

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
    def mass_disc_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7068.MassDiscCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7068,
        )

        return self.__parent__._cast(_7068.MassDiscCompoundCriticalSpeedAnalysis)

    @property
    def measurement_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7069.MeasurementComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7069,
        )

        return self.__parent__._cast(
            _7069.MeasurementComponentCompoundCriticalSpeedAnalysis
        )

    @property
    def oil_seal_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7073.OilSealCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7073,
        )

        return self.__parent__._cast(_7073.OilSealCompoundCriticalSpeedAnalysis)

    @property
    def part_to_part_shear_coupling_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7077.PartToPartShearCouplingHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7077,
        )

        return self.__parent__._cast(
            _7077.PartToPartShearCouplingHalfCompoundCriticalSpeedAnalysis
        )

    @property
    def planet_carrier_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7080.PlanetCarrierCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7080,
        )

        return self.__parent__._cast(_7080.PlanetCarrierCompoundCriticalSpeedAnalysis)

    @property
    def point_load_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7081.PointLoadCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7081,
        )

        return self.__parent__._cast(_7081.PointLoadCompoundCriticalSpeedAnalysis)

    @property
    def power_load_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7082.PowerLoadCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7082,
        )

        return self.__parent__._cast(_7082.PowerLoadCompoundCriticalSpeedAnalysis)

    @property
    def pulley_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7083.PulleyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7083,
        )

        return self.__parent__._cast(_7083.PulleyCompoundCriticalSpeedAnalysis)

    @property
    def ring_pins_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7084.RingPinsCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7084,
        )

        return self.__parent__._cast(_7084.RingPinsCompoundCriticalSpeedAnalysis)

    @property
    def rolling_ring_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7087.RollingRingCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7087,
        )

        return self.__parent__._cast(_7087.RollingRingCompoundCriticalSpeedAnalysis)

    @property
    def shaft_hub_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7091.ShaftHubConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7091,
        )

        return self.__parent__._cast(
            _7091.ShaftHubConnectionCompoundCriticalSpeedAnalysis
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
    def spring_damper_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7099.SpringDamperHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7099,
        )

        return self.__parent__._cast(
            _7099.SpringDamperHalfCompoundCriticalSpeedAnalysis
        )

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
    def synchroniser_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7109.SynchroniserHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7109,
        )

        return self.__parent__._cast(
            _7109.SynchroniserHalfCompoundCriticalSpeedAnalysis
        )

    @property
    def synchroniser_part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7110.SynchroniserPartCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7110,
        )

        return self.__parent__._cast(
            _7110.SynchroniserPartCompoundCriticalSpeedAnalysis
        )

    @property
    def synchroniser_sleeve_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7111.SynchroniserSleeveCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7111,
        )

        return self.__parent__._cast(
            _7111.SynchroniserSleeveCompoundCriticalSpeedAnalysis
        )

    @property
    def torque_converter_pump_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7114.TorqueConverterPumpCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7114,
        )

        return self.__parent__._cast(
            _7114.TorqueConverterPumpCompoundCriticalSpeedAnalysis
        )

    @property
    def torque_converter_turbine_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7115.TorqueConverterTurbineCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7115,
        )

        return self.__parent__._cast(
            _7115.TorqueConverterTurbineCompoundCriticalSpeedAnalysis
        )

    @property
    def unbalanced_mass_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7116.UnbalancedMassCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7116,
        )

        return self.__parent__._cast(_7116.UnbalancedMassCompoundCriticalSpeedAnalysis)

    @property
    def virtual_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7117.VirtualComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7117,
        )

        return self.__parent__._cast(
            _7117.VirtualComponentCompoundCriticalSpeedAnalysis
        )

    @property
    def worm_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7118.WormGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7118,
        )

        return self.__parent__._cast(_7118.WormGearCompoundCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7121.ZerolBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7121,
        )

        return self.__parent__._cast(_7121.ZerolBevelGearCompoundCriticalSpeedAnalysis)

    @property
    def mountable_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "MountableComponentCompoundCriticalSpeedAnalysis":
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
class MountableComponentCompoundCriticalSpeedAnalysis(
    _7018.ComponentCompoundCriticalSpeedAnalysis
):
    """MountableComponentCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6941.MountableComponentCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.MountableComponentCriticalSpeedAnalysis]

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
    ) -> "List[_6941.MountableComponentCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.MountableComponentCriticalSpeedAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_MountableComponentCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentCompoundCriticalSpeedAnalysis
        """
        return _Cast_MountableComponentCompoundCriticalSpeedAnalysis(self)
