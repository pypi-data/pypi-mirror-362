"""ComponentSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _3028

_COMPONENT_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "ComponentSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.materials.efficiency import _391, _392
    from mastapy._private.math_utility import _1702
    from mastapy._private.math_utility.measured_vectors import _1745, _1746
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7889,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4318
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2927,
        _2928,
        _2932,
        _2939,
        _2944,
        _2945,
        _2946,
        _2949,
        _2951,
        _2953,
        _2959,
        _2963,
        _2967,
        _2969,
        _2971,
        _2974,
        _2979,
        _2986,
        _2987,
        _2988,
        _2991,
        _2992,
        _2993,
        _2997,
        _2998,
        _3002,
        _3003,
        _3006,
        _3011,
        _3014,
        _3017,
        _3020,
        _3021,
        _3024,
        _3025,
        _3027,
        _3030,
        _3033,
        _3034,
        _3035,
        _3036,
        _3037,
        _3042,
        _3044,
        _3047,
        _3052,
        _3054,
        _3058,
        _3061,
        _3062,
        _3063,
        _3064,
        _3065,
        _3066,
        _3072,
        _3074,
        _3077,
        _3078,
        _3081,
        _3084,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3091,
    )
    from mastapy._private.system_model.part_model import _2670

    Self = TypeVar("Self", bound="ComponentSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf", bound="ComponentSystemDeflection._Cast_ComponentSystemDeflection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentSystemDeflection:
    """Special nested class for casting ComponentSystemDeflection to subclasses."""

    __parent__: "ComponentSystemDeflection"

    @property
    def part_system_deflection(self: "CastSelf") -> "_3028.PartSystemDeflection":
        return self.__parent__._cast(_3028.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7889.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7889,
        )

        return self.__parent__._cast(_7889.PartFEAnalysis)

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
    def abstract_shaft_or_housing_system_deflection(
        self: "CastSelf",
    ) -> "_2927.AbstractShaftOrHousingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2927,
        )

        return self.__parent__._cast(_2927.AbstractShaftOrHousingSystemDeflection)

    @property
    def abstract_shaft_system_deflection(
        self: "CastSelf",
    ) -> "_2928.AbstractShaftSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2928,
        )

        return self.__parent__._cast(_2928.AbstractShaftSystemDeflection)

    @property
    def agma_gleason_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2932.AGMAGleasonConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2932,
        )

        return self.__parent__._cast(_2932.AGMAGleasonConicalGearSystemDeflection)

    @property
    def bearing_system_deflection(self: "CastSelf") -> "_2939.BearingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2939,
        )

        return self.__parent__._cast(_2939.BearingSystemDeflection)

    @property
    def bevel_differential_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2944.BevelDifferentialGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2944,
        )

        return self.__parent__._cast(_2944.BevelDifferentialGearSystemDeflection)

    @property
    def bevel_differential_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2945.BevelDifferentialPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2945,
        )

        return self.__parent__._cast(_2945.BevelDifferentialPlanetGearSystemDeflection)

    @property
    def bevel_differential_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2946.BevelDifferentialSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2946,
        )

        return self.__parent__._cast(_2946.BevelDifferentialSunGearSystemDeflection)

    @property
    def bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2949.BevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2949,
        )

        return self.__parent__._cast(_2949.BevelGearSystemDeflection)

    @property
    def bolt_system_deflection(self: "CastSelf") -> "_2951.BoltSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2951,
        )

        return self.__parent__._cast(_2951.BoltSystemDeflection)

    @property
    def clutch_half_system_deflection(
        self: "CastSelf",
    ) -> "_2953.ClutchHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2953,
        )

        return self.__parent__._cast(_2953.ClutchHalfSystemDeflection)

    @property
    def concept_coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2959.ConceptCouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2959,
        )

        return self.__parent__._cast(_2959.ConceptCouplingHalfSystemDeflection)

    @property
    def concept_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2963.ConceptGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2963,
        )

        return self.__parent__._cast(_2963.ConceptGearSystemDeflection)

    @property
    def conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2967.ConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2967,
        )

        return self.__parent__._cast(_2967.ConicalGearSystemDeflection)

    @property
    def connector_system_deflection(
        self: "CastSelf",
    ) -> "_2969.ConnectorSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2969,
        )

        return self.__parent__._cast(_2969.ConnectorSystemDeflection)

    @property
    def coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2971.CouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2971,
        )

        return self.__parent__._cast(_2971.CouplingHalfSystemDeflection)

    @property
    def cvt_pulley_system_deflection(
        self: "CastSelf",
    ) -> "_2974.CVTPulleySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2974,
        )

        return self.__parent__._cast(_2974.CVTPulleySystemDeflection)

    @property
    def cycloidal_disc_system_deflection(
        self: "CastSelf",
    ) -> "_2979.CycloidalDiscSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2979,
        )

        return self.__parent__._cast(_2979.CycloidalDiscSystemDeflection)

    @property
    def cylindrical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2986.CylindricalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2986,
        )

        return self.__parent__._cast(_2986.CylindricalGearSystemDeflection)

    @property
    def cylindrical_gear_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2987.CylindricalGearSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2987,
        )

        return self.__parent__._cast(_2987.CylindricalGearSystemDeflectionTimestep)

    @property
    def cylindrical_gear_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2988.CylindricalGearSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2988,
        )

        return self.__parent__._cast(
            _2988.CylindricalGearSystemDeflectionWithLTCAResults
        )

    @property
    def cylindrical_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2991.CylindricalPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2991,
        )

        return self.__parent__._cast(_2991.CylindricalPlanetGearSystemDeflection)

    @property
    def datum_system_deflection(self: "CastSelf") -> "_2992.DatumSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2992,
        )

        return self.__parent__._cast(_2992.DatumSystemDeflection)

    @property
    def external_cad_model_system_deflection(
        self: "CastSelf",
    ) -> "_2993.ExternalCADModelSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2993,
        )

        return self.__parent__._cast(_2993.ExternalCADModelSystemDeflection)

    @property
    def face_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2997.FaceGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2997,
        )

        return self.__parent__._cast(_2997.FaceGearSystemDeflection)

    @property
    def fe_part_system_deflection(self: "CastSelf") -> "_2998.FEPartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2998,
        )

        return self.__parent__._cast(_2998.FEPartSystemDeflection)

    @property
    def gear_system_deflection(self: "CastSelf") -> "_3002.GearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3002,
        )

        return self.__parent__._cast(_3002.GearSystemDeflection)

    @property
    def guide_dxf_model_system_deflection(
        self: "CastSelf",
    ) -> "_3003.GuideDxfModelSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3003,
        )

        return self.__parent__._cast(_3003.GuideDxfModelSystemDeflection)

    @property
    def hypoid_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3006.HypoidGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3006,
        )

        return self.__parent__._cast(_3006.HypoidGearSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3011.KlingelnbergCycloPalloidConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3011,
        )

        return self.__parent__._cast(
            _3011.KlingelnbergCycloPalloidConicalGearSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3014.KlingelnbergCycloPalloidHypoidGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3014,
        )

        return self.__parent__._cast(
            _3014.KlingelnbergCycloPalloidHypoidGearSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3017.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3017,
        )

        return self.__parent__._cast(
            _3017.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection
        )

    @property
    def mass_disc_system_deflection(
        self: "CastSelf",
    ) -> "_3020.MassDiscSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3020,
        )

        return self.__parent__._cast(_3020.MassDiscSystemDeflection)

    @property
    def measurement_component_system_deflection(
        self: "CastSelf",
    ) -> "_3021.MeasurementComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3021,
        )

        return self.__parent__._cast(_3021.MeasurementComponentSystemDeflection)

    @property
    def microphone_system_deflection(
        self: "CastSelf",
    ) -> "_3024.MicrophoneSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3024,
        )

        return self.__parent__._cast(_3024.MicrophoneSystemDeflection)

    @property
    def mountable_component_system_deflection(
        self: "CastSelf",
    ) -> "_3025.MountableComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3025,
        )

        return self.__parent__._cast(_3025.MountableComponentSystemDeflection)

    @property
    def oil_seal_system_deflection(self: "CastSelf") -> "_3027.OilSealSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3027,
        )

        return self.__parent__._cast(_3027.OilSealSystemDeflection)

    @property
    def part_to_part_shear_coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_3030.PartToPartShearCouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3030,
        )

        return self.__parent__._cast(_3030.PartToPartShearCouplingHalfSystemDeflection)

    @property
    def planet_carrier_system_deflection(
        self: "CastSelf",
    ) -> "_3033.PlanetCarrierSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3033,
        )

        return self.__parent__._cast(_3033.PlanetCarrierSystemDeflection)

    @property
    def point_load_system_deflection(
        self: "CastSelf",
    ) -> "_3034.PointLoadSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3034,
        )

        return self.__parent__._cast(_3034.PointLoadSystemDeflection)

    @property
    def power_load_system_deflection(
        self: "CastSelf",
    ) -> "_3035.PowerLoadSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3035,
        )

        return self.__parent__._cast(_3035.PowerLoadSystemDeflection)

    @property
    def pulley_system_deflection(self: "CastSelf") -> "_3036.PulleySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3036,
        )

        return self.__parent__._cast(_3036.PulleySystemDeflection)

    @property
    def ring_pins_system_deflection(
        self: "CastSelf",
    ) -> "_3037.RingPinsSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3037,
        )

        return self.__parent__._cast(_3037.RingPinsSystemDeflection)

    @property
    def rolling_ring_system_deflection(
        self: "CastSelf",
    ) -> "_3042.RollingRingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3042,
        )

        return self.__parent__._cast(_3042.RollingRingSystemDeflection)

    @property
    def shaft_hub_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3044.ShaftHubConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3044,
        )

        return self.__parent__._cast(_3044.ShaftHubConnectionSystemDeflection)

    @property
    def shaft_system_deflection(self: "CastSelf") -> "_3047.ShaftSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3047,
        )

        return self.__parent__._cast(_3047.ShaftSystemDeflection)

    @property
    def spiral_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3052.SpiralBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3052,
        )

        return self.__parent__._cast(_3052.SpiralBevelGearSystemDeflection)

    @property
    def spring_damper_half_system_deflection(
        self: "CastSelf",
    ) -> "_3054.SpringDamperHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3054,
        )

        return self.__parent__._cast(_3054.SpringDamperHalfSystemDeflection)

    @property
    def straight_bevel_diff_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3058.StraightBevelDiffGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3058,
        )

        return self.__parent__._cast(_3058.StraightBevelDiffGearSystemDeflection)

    @property
    def straight_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3061.StraightBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3061,
        )

        return self.__parent__._cast(_3061.StraightBevelGearSystemDeflection)

    @property
    def straight_bevel_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3062.StraightBevelPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3062,
        )

        return self.__parent__._cast(_3062.StraightBevelPlanetGearSystemDeflection)

    @property
    def straight_bevel_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3063.StraightBevelSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3063,
        )

        return self.__parent__._cast(_3063.StraightBevelSunGearSystemDeflection)

    @property
    def synchroniser_half_system_deflection(
        self: "CastSelf",
    ) -> "_3064.SynchroniserHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3064,
        )

        return self.__parent__._cast(_3064.SynchroniserHalfSystemDeflection)

    @property
    def synchroniser_part_system_deflection(
        self: "CastSelf",
    ) -> "_3065.SynchroniserPartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3065,
        )

        return self.__parent__._cast(_3065.SynchroniserPartSystemDeflection)

    @property
    def synchroniser_sleeve_system_deflection(
        self: "CastSelf",
    ) -> "_3066.SynchroniserSleeveSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3066,
        )

        return self.__parent__._cast(_3066.SynchroniserSleeveSystemDeflection)

    @property
    def torque_converter_pump_system_deflection(
        self: "CastSelf",
    ) -> "_3072.TorqueConverterPumpSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3072,
        )

        return self.__parent__._cast(_3072.TorqueConverterPumpSystemDeflection)

    @property
    def torque_converter_turbine_system_deflection(
        self: "CastSelf",
    ) -> "_3074.TorqueConverterTurbineSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3074,
        )

        return self.__parent__._cast(_3074.TorqueConverterTurbineSystemDeflection)

    @property
    def unbalanced_mass_system_deflection(
        self: "CastSelf",
    ) -> "_3077.UnbalancedMassSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3077,
        )

        return self.__parent__._cast(_3077.UnbalancedMassSystemDeflection)

    @property
    def virtual_component_system_deflection(
        self: "CastSelf",
    ) -> "_3078.VirtualComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3078,
        )

        return self.__parent__._cast(_3078.VirtualComponentSystemDeflection)

    @property
    def worm_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3081.WormGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3081,
        )

        return self.__parent__._cast(_3081.WormGearSystemDeflection)

    @property
    def zerol_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3084.ZerolBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3084,
        )

        return self.__parent__._cast(_3084.ZerolBevelGearSystemDeflection)

    @property
    def component_system_deflection(self: "CastSelf") -> "ComponentSystemDeflection":
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
class ComponentSystemDeflection(_3028.PartSystemDeflection):
    """ComponentSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def energy_loss_during_load_case(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnergyLossDuringLoadCase")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def has_converged(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasConverged")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def percentage_of_iterations_converged(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PercentageOfIterationsConverged")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reason_for_non_convergence(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReasonForNonConvergence")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def reason_mass_properties_are_unknown(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReasonMassPropertiesAreUnknown")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def reason_mass_properties_are_zero(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReasonMassPropertiesAreZero")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def relaxation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Relaxation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2670.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mass_properties_in_local_coordinate_system_from_node_model(
        self: "Self",
    ) -> "_1702.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MassPropertiesInLocalCoordinateSystemFromNodeModel"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def power_loss(self: "Self") -> "_391.PowerLoss":
        """mastapy.materials.efficiency.PowerLoss

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLoss")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def resistive_torque(self: "Self") -> "_392.ResistiveTorque":
        """mastapy.materials.efficiency.ResistiveTorque

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResistiveTorque")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rigidly_connected_components(
        self: "Self",
    ) -> "_3091.RigidlyConnectedComponentGroupSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.reporting.RigidlyConnectedComponentGroupSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RigidlyConnectedComponents")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connected_components_forces_in_lcs(self: "Self") -> "List[_1745.ForceResults]":
        """List[mastapy.math_utility.measured_vectors.ForceResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectedComponentsForcesInLCS")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def connected_components_forces_in_wcs(self: "Self") -> "List[_1745.ForceResults]":
        """List[mastapy.math_utility.measured_vectors.ForceResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectedComponentsForcesInWCS")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def node_results(self: "Self") -> "List[_1746.NodeResults]":
        """List[mastapy.math_utility.measured_vectors.NodeResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def power_flow_results(self: "Self") -> "_4318.ComponentPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.ComponentPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ComponentSystemDeflection
        """
        return _Cast_ComponentSystemDeflection(self)
