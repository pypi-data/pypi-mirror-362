"""ComponentCompoundStabilityAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4237,
)

_COMPONENT_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "ComponentCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4045,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4157,
        _4158,
        _4160,
        _4164,
        _4167,
        _4170,
        _4171,
        _4172,
        _4175,
        _4179,
        _4184,
        _4185,
        _4188,
        _4192,
        _4195,
        _4198,
        _4201,
        _4203,
        _4206,
        _4207,
        _4208,
        _4209,
        _4212,
        _4214,
        _4217,
        _4218,
        _4222,
        _4225,
        _4228,
        _4231,
        _4232,
        _4234,
        _4235,
        _4236,
        _4240,
        _4243,
        _4244,
        _4245,
        _4246,
        _4247,
        _4250,
        _4253,
        _4254,
        _4257,
        _4262,
        _4263,
        _4266,
        _4269,
        _4270,
        _4272,
        _4273,
        _4274,
        _4277,
        _4278,
        _4279,
        _4280,
        _4281,
        _4284,
    )

    Self = TypeVar("Self", bound="ComponentCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ComponentCompoundStabilityAnalysis._Cast_ComponentCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentCompoundStabilityAnalysis:
    """Special nested class for casting ComponentCompoundStabilityAnalysis to subclasses."""

    __parent__: "ComponentCompoundStabilityAnalysis"

    @property
    def part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4237.PartCompoundStabilityAnalysis":
        return self.__parent__._cast(_4237.PartCompoundStabilityAnalysis)

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
    def abstract_shaft_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4157.AbstractShaftCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4157,
        )

        return self.__parent__._cast(_4157.AbstractShaftCompoundStabilityAnalysis)

    @property
    def abstract_shaft_or_housing_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4158.AbstractShaftOrHousingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4158,
        )

        return self.__parent__._cast(
            _4158.AbstractShaftOrHousingCompoundStabilityAnalysis
        )

    @property
    def agma_gleason_conical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4160.AGMAGleasonConicalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4160,
        )

        return self.__parent__._cast(
            _4160.AGMAGleasonConicalGearCompoundStabilityAnalysis
        )

    @property
    def bearing_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4164.BearingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4164,
        )

        return self.__parent__._cast(_4164.BearingCompoundStabilityAnalysis)

    @property
    def bevel_differential_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4167.BevelDifferentialGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4167,
        )

        return self.__parent__._cast(
            _4167.BevelDifferentialGearCompoundStabilityAnalysis
        )

    @property
    def bevel_differential_planet_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4170.BevelDifferentialPlanetGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4170,
        )

        return self.__parent__._cast(
            _4170.BevelDifferentialPlanetGearCompoundStabilityAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4171.BevelDifferentialSunGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4171,
        )

        return self.__parent__._cast(
            _4171.BevelDifferentialSunGearCompoundStabilityAnalysis
        )

    @property
    def bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4172.BevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4172,
        )

        return self.__parent__._cast(_4172.BevelGearCompoundStabilityAnalysis)

    @property
    def bolt_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4175.BoltCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4175,
        )

        return self.__parent__._cast(_4175.BoltCompoundStabilityAnalysis)

    @property
    def clutch_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4179.ClutchHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4179,
        )

        return self.__parent__._cast(_4179.ClutchHalfCompoundStabilityAnalysis)

    @property
    def concept_coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4184.ConceptCouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4184,
        )

        return self.__parent__._cast(_4184.ConceptCouplingHalfCompoundStabilityAnalysis)

    @property
    def concept_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4185.ConceptGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4185,
        )

        return self.__parent__._cast(_4185.ConceptGearCompoundStabilityAnalysis)

    @property
    def conical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4188.ConicalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4188,
        )

        return self.__parent__._cast(_4188.ConicalGearCompoundStabilityAnalysis)

    @property
    def connector_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4192.ConnectorCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4192,
        )

        return self.__parent__._cast(_4192.ConnectorCompoundStabilityAnalysis)

    @property
    def coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4195.CouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4195,
        )

        return self.__parent__._cast(_4195.CouplingHalfCompoundStabilityAnalysis)

    @property
    def cvt_pulley_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4198.CVTPulleyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4198,
        )

        return self.__parent__._cast(_4198.CVTPulleyCompoundStabilityAnalysis)

    @property
    def cycloidal_disc_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4201.CycloidalDiscCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4201,
        )

        return self.__parent__._cast(_4201.CycloidalDiscCompoundStabilityAnalysis)

    @property
    def cylindrical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4203.CylindricalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4203,
        )

        return self.__parent__._cast(_4203.CylindricalGearCompoundStabilityAnalysis)

    @property
    def cylindrical_planet_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4206.CylindricalPlanetGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4206,
        )

        return self.__parent__._cast(
            _4206.CylindricalPlanetGearCompoundStabilityAnalysis
        )

    @property
    def datum_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4207.DatumCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4207,
        )

        return self.__parent__._cast(_4207.DatumCompoundStabilityAnalysis)

    @property
    def external_cad_model_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4208.ExternalCADModelCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4208,
        )

        return self.__parent__._cast(_4208.ExternalCADModelCompoundStabilityAnalysis)

    @property
    def face_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4209.FaceGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4209,
        )

        return self.__parent__._cast(_4209.FaceGearCompoundStabilityAnalysis)

    @property
    def fe_part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4212.FEPartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4212,
        )

        return self.__parent__._cast(_4212.FEPartCompoundStabilityAnalysis)

    @property
    def gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4214.GearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4214,
        )

        return self.__parent__._cast(_4214.GearCompoundStabilityAnalysis)

    @property
    def guide_dxf_model_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4217.GuideDxfModelCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4217,
        )

        return self.__parent__._cast(_4217.GuideDxfModelCompoundStabilityAnalysis)

    @property
    def hypoid_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4218.HypoidGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4218,
        )

        return self.__parent__._cast(_4218.HypoidGearCompoundStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4222.KlingelnbergCycloPalloidConicalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4222,
        )

        return self.__parent__._cast(
            _4222.KlingelnbergCycloPalloidConicalGearCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4225.KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4225,
        )

        return self.__parent__._cast(
            _4225.KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4228.KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4228,
        )

        return self.__parent__._cast(
            _4228.KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis
        )

    @property
    def mass_disc_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4231.MassDiscCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4231,
        )

        return self.__parent__._cast(_4231.MassDiscCompoundStabilityAnalysis)

    @property
    def measurement_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4232.MeasurementComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4232,
        )

        return self.__parent__._cast(
            _4232.MeasurementComponentCompoundStabilityAnalysis
        )

    @property
    def microphone_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4234.MicrophoneCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4234,
        )

        return self.__parent__._cast(_4234.MicrophoneCompoundStabilityAnalysis)

    @property
    def mountable_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4235.MountableComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4235,
        )

        return self.__parent__._cast(_4235.MountableComponentCompoundStabilityAnalysis)

    @property
    def oil_seal_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4236.OilSealCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4236,
        )

        return self.__parent__._cast(_4236.OilSealCompoundStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4240.PartToPartShearCouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4240,
        )

        return self.__parent__._cast(
            _4240.PartToPartShearCouplingHalfCompoundStabilityAnalysis
        )

    @property
    def planet_carrier_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4243.PlanetCarrierCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4243,
        )

        return self.__parent__._cast(_4243.PlanetCarrierCompoundStabilityAnalysis)

    @property
    def point_load_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4244.PointLoadCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4244,
        )

        return self.__parent__._cast(_4244.PointLoadCompoundStabilityAnalysis)

    @property
    def power_load_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4245.PowerLoadCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4245,
        )

        return self.__parent__._cast(_4245.PowerLoadCompoundStabilityAnalysis)

    @property
    def pulley_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4246.PulleyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4246,
        )

        return self.__parent__._cast(_4246.PulleyCompoundStabilityAnalysis)

    @property
    def ring_pins_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4247.RingPinsCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4247,
        )

        return self.__parent__._cast(_4247.RingPinsCompoundStabilityAnalysis)

    @property
    def rolling_ring_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4250.RollingRingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4250,
        )

        return self.__parent__._cast(_4250.RollingRingCompoundStabilityAnalysis)

    @property
    def shaft_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4253.ShaftCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4253,
        )

        return self.__parent__._cast(_4253.ShaftCompoundStabilityAnalysis)

    @property
    def shaft_hub_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4254.ShaftHubConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4254,
        )

        return self.__parent__._cast(_4254.ShaftHubConnectionCompoundStabilityAnalysis)

    @property
    def spiral_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4257.SpiralBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4257,
        )

        return self.__parent__._cast(_4257.SpiralBevelGearCompoundStabilityAnalysis)

    @property
    def spring_damper_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4262.SpringDamperHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4262,
        )

        return self.__parent__._cast(_4262.SpringDamperHalfCompoundStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4263.StraightBevelDiffGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4263,
        )

        return self.__parent__._cast(
            _4263.StraightBevelDiffGearCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4266.StraightBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4266,
        )

        return self.__parent__._cast(_4266.StraightBevelGearCompoundStabilityAnalysis)

    @property
    def straight_bevel_planet_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4269.StraightBevelPlanetGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4269,
        )

        return self.__parent__._cast(
            _4269.StraightBevelPlanetGearCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4270.StraightBevelSunGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4270,
        )

        return self.__parent__._cast(
            _4270.StraightBevelSunGearCompoundStabilityAnalysis
        )

    @property
    def synchroniser_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4272.SynchroniserHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4272,
        )

        return self.__parent__._cast(_4272.SynchroniserHalfCompoundStabilityAnalysis)

    @property
    def synchroniser_part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4273.SynchroniserPartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4273,
        )

        return self.__parent__._cast(_4273.SynchroniserPartCompoundStabilityAnalysis)

    @property
    def synchroniser_sleeve_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4274.SynchroniserSleeveCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4274,
        )

        return self.__parent__._cast(_4274.SynchroniserSleeveCompoundStabilityAnalysis)

    @property
    def torque_converter_pump_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4277.TorqueConverterPumpCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4277,
        )

        return self.__parent__._cast(_4277.TorqueConverterPumpCompoundStabilityAnalysis)

    @property
    def torque_converter_turbine_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4278.TorqueConverterTurbineCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4278,
        )

        return self.__parent__._cast(
            _4278.TorqueConverterTurbineCompoundStabilityAnalysis
        )

    @property
    def unbalanced_mass_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4279.UnbalancedMassCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4279,
        )

        return self.__parent__._cast(_4279.UnbalancedMassCompoundStabilityAnalysis)

    @property
    def virtual_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4280.VirtualComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4280,
        )

        return self.__parent__._cast(_4280.VirtualComponentCompoundStabilityAnalysis)

    @property
    def worm_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4281.WormGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4281,
        )

        return self.__parent__._cast(_4281.WormGearCompoundStabilityAnalysis)

    @property
    def zerol_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4284.ZerolBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4284,
        )

        return self.__parent__._cast(_4284.ZerolBevelGearCompoundStabilityAnalysis)

    @property
    def component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "ComponentCompoundStabilityAnalysis":
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
class ComponentCompoundStabilityAnalysis(_4237.PartCompoundStabilityAnalysis):
    """ComponentCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_COMPOUND_STABILITY_ANALYSIS

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
    ) -> "List[_4045.ComponentStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.ComponentStabilityAnalysis]

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
    ) -> "List[_4045.ComponentStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.ComponentStabilityAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ComponentCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ComponentCompoundStabilityAnalysis
        """
        return _Cast_ComponentCompoundStabilityAnalysis(self)
