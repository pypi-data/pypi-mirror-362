"""ComponentCompoundPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4511,
)

_COMPONENT_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "ComponentCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4318
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4431,
        _4432,
        _4434,
        _4438,
        _4441,
        _4444,
        _4445,
        _4446,
        _4449,
        _4453,
        _4458,
        _4459,
        _4462,
        _4466,
        _4469,
        _4472,
        _4475,
        _4477,
        _4480,
        _4481,
        _4482,
        _4483,
        _4486,
        _4488,
        _4491,
        _4492,
        _4496,
        _4499,
        _4502,
        _4505,
        _4506,
        _4508,
        _4509,
        _4510,
        _4514,
        _4517,
        _4518,
        _4519,
        _4520,
        _4521,
        _4524,
        _4527,
        _4528,
        _4531,
        _4536,
        _4537,
        _4540,
        _4543,
        _4544,
        _4546,
        _4547,
        _4548,
        _4551,
        _4552,
        _4553,
        _4554,
        _4555,
        _4558,
    )

    Self = TypeVar("Self", bound="ComponentCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="ComponentCompoundPowerFlow._Cast_ComponentCompoundPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentCompoundPowerFlow:
    """Special nested class for casting ComponentCompoundPowerFlow to subclasses."""

    __parent__: "ComponentCompoundPowerFlow"

    @property
    def part_compound_power_flow(self: "CastSelf") -> "_4511.PartCompoundPowerFlow":
        return self.__parent__._cast(_4511.PartCompoundPowerFlow)

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
    def abstract_shaft_compound_power_flow(
        self: "CastSelf",
    ) -> "_4431.AbstractShaftCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4431,
        )

        return self.__parent__._cast(_4431.AbstractShaftCompoundPowerFlow)

    @property
    def abstract_shaft_or_housing_compound_power_flow(
        self: "CastSelf",
    ) -> "_4432.AbstractShaftOrHousingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4432,
        )

        return self.__parent__._cast(_4432.AbstractShaftOrHousingCompoundPowerFlow)

    @property
    def agma_gleason_conical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4434.AGMAGleasonConicalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4434,
        )

        return self.__parent__._cast(_4434.AGMAGleasonConicalGearCompoundPowerFlow)

    @property
    def bearing_compound_power_flow(
        self: "CastSelf",
    ) -> "_4438.BearingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4438,
        )

        return self.__parent__._cast(_4438.BearingCompoundPowerFlow)

    @property
    def bevel_differential_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4441.BevelDifferentialGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4441,
        )

        return self.__parent__._cast(_4441.BevelDifferentialGearCompoundPowerFlow)

    @property
    def bevel_differential_planet_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4444.BevelDifferentialPlanetGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4444,
        )

        return self.__parent__._cast(_4444.BevelDifferentialPlanetGearCompoundPowerFlow)

    @property
    def bevel_differential_sun_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4445.BevelDifferentialSunGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4445,
        )

        return self.__parent__._cast(_4445.BevelDifferentialSunGearCompoundPowerFlow)

    @property
    def bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4446.BevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4446,
        )

        return self.__parent__._cast(_4446.BevelGearCompoundPowerFlow)

    @property
    def bolt_compound_power_flow(self: "CastSelf") -> "_4449.BoltCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4449,
        )

        return self.__parent__._cast(_4449.BoltCompoundPowerFlow)

    @property
    def clutch_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4453.ClutchHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4453,
        )

        return self.__parent__._cast(_4453.ClutchHalfCompoundPowerFlow)

    @property
    def concept_coupling_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4458.ConceptCouplingHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4458,
        )

        return self.__parent__._cast(_4458.ConceptCouplingHalfCompoundPowerFlow)

    @property
    def concept_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4459.ConceptGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4459,
        )

        return self.__parent__._cast(_4459.ConceptGearCompoundPowerFlow)

    @property
    def conical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4462.ConicalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4462,
        )

        return self.__parent__._cast(_4462.ConicalGearCompoundPowerFlow)

    @property
    def connector_compound_power_flow(
        self: "CastSelf",
    ) -> "_4466.ConnectorCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4466,
        )

        return self.__parent__._cast(_4466.ConnectorCompoundPowerFlow)

    @property
    def coupling_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4469.CouplingHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4469,
        )

        return self.__parent__._cast(_4469.CouplingHalfCompoundPowerFlow)

    @property
    def cvt_pulley_compound_power_flow(
        self: "CastSelf",
    ) -> "_4472.CVTPulleyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4472,
        )

        return self.__parent__._cast(_4472.CVTPulleyCompoundPowerFlow)

    @property
    def cycloidal_disc_compound_power_flow(
        self: "CastSelf",
    ) -> "_4475.CycloidalDiscCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4475,
        )

        return self.__parent__._cast(_4475.CycloidalDiscCompoundPowerFlow)

    @property
    def cylindrical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4477.CylindricalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4477,
        )

        return self.__parent__._cast(_4477.CylindricalGearCompoundPowerFlow)

    @property
    def cylindrical_planet_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4480.CylindricalPlanetGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4480,
        )

        return self.__parent__._cast(_4480.CylindricalPlanetGearCompoundPowerFlow)

    @property
    def datum_compound_power_flow(self: "CastSelf") -> "_4481.DatumCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4481,
        )

        return self.__parent__._cast(_4481.DatumCompoundPowerFlow)

    @property
    def external_cad_model_compound_power_flow(
        self: "CastSelf",
    ) -> "_4482.ExternalCADModelCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4482,
        )

        return self.__parent__._cast(_4482.ExternalCADModelCompoundPowerFlow)

    @property
    def face_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4483.FaceGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4483,
        )

        return self.__parent__._cast(_4483.FaceGearCompoundPowerFlow)

    @property
    def fe_part_compound_power_flow(
        self: "CastSelf",
    ) -> "_4486.FEPartCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4486,
        )

        return self.__parent__._cast(_4486.FEPartCompoundPowerFlow)

    @property
    def gear_compound_power_flow(self: "CastSelf") -> "_4488.GearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4488,
        )

        return self.__parent__._cast(_4488.GearCompoundPowerFlow)

    @property
    def guide_dxf_model_compound_power_flow(
        self: "CastSelf",
    ) -> "_4491.GuideDxfModelCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4491,
        )

        return self.__parent__._cast(_4491.GuideDxfModelCompoundPowerFlow)

    @property
    def hypoid_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4492.HypoidGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4492,
        )

        return self.__parent__._cast(_4492.HypoidGearCompoundPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4496.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4496,
        )

        return self.__parent__._cast(
            _4496.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4499.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4499,
        )

        return self.__parent__._cast(
            _4499.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4502.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4502,
        )

        return self.__parent__._cast(
            _4502.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow
        )

    @property
    def mass_disc_compound_power_flow(
        self: "CastSelf",
    ) -> "_4505.MassDiscCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4505,
        )

        return self.__parent__._cast(_4505.MassDiscCompoundPowerFlow)

    @property
    def measurement_component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4506.MeasurementComponentCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4506,
        )

        return self.__parent__._cast(_4506.MeasurementComponentCompoundPowerFlow)

    @property
    def microphone_compound_power_flow(
        self: "CastSelf",
    ) -> "_4508.MicrophoneCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4508,
        )

        return self.__parent__._cast(_4508.MicrophoneCompoundPowerFlow)

    @property
    def mountable_component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4509.MountableComponentCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4509,
        )

        return self.__parent__._cast(_4509.MountableComponentCompoundPowerFlow)

    @property
    def oil_seal_compound_power_flow(
        self: "CastSelf",
    ) -> "_4510.OilSealCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4510,
        )

        return self.__parent__._cast(_4510.OilSealCompoundPowerFlow)

    @property
    def part_to_part_shear_coupling_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4514.PartToPartShearCouplingHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4514,
        )

        return self.__parent__._cast(_4514.PartToPartShearCouplingHalfCompoundPowerFlow)

    @property
    def planet_carrier_compound_power_flow(
        self: "CastSelf",
    ) -> "_4517.PlanetCarrierCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4517,
        )

        return self.__parent__._cast(_4517.PlanetCarrierCompoundPowerFlow)

    @property
    def point_load_compound_power_flow(
        self: "CastSelf",
    ) -> "_4518.PointLoadCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4518,
        )

        return self.__parent__._cast(_4518.PointLoadCompoundPowerFlow)

    @property
    def power_load_compound_power_flow(
        self: "CastSelf",
    ) -> "_4519.PowerLoadCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4519,
        )

        return self.__parent__._cast(_4519.PowerLoadCompoundPowerFlow)

    @property
    def pulley_compound_power_flow(self: "CastSelf") -> "_4520.PulleyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4520,
        )

        return self.__parent__._cast(_4520.PulleyCompoundPowerFlow)

    @property
    def ring_pins_compound_power_flow(
        self: "CastSelf",
    ) -> "_4521.RingPinsCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4521,
        )

        return self.__parent__._cast(_4521.RingPinsCompoundPowerFlow)

    @property
    def rolling_ring_compound_power_flow(
        self: "CastSelf",
    ) -> "_4524.RollingRingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4524,
        )

        return self.__parent__._cast(_4524.RollingRingCompoundPowerFlow)

    @property
    def shaft_compound_power_flow(self: "CastSelf") -> "_4527.ShaftCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4527,
        )

        return self.__parent__._cast(_4527.ShaftCompoundPowerFlow)

    @property
    def shaft_hub_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4528.ShaftHubConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4528,
        )

        return self.__parent__._cast(_4528.ShaftHubConnectionCompoundPowerFlow)

    @property
    def spiral_bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4531.SpiralBevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4531,
        )

        return self.__parent__._cast(_4531.SpiralBevelGearCompoundPowerFlow)

    @property
    def spring_damper_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4536.SpringDamperHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4536,
        )

        return self.__parent__._cast(_4536.SpringDamperHalfCompoundPowerFlow)

    @property
    def straight_bevel_diff_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4537.StraightBevelDiffGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4537,
        )

        return self.__parent__._cast(_4537.StraightBevelDiffGearCompoundPowerFlow)

    @property
    def straight_bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4540.StraightBevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4540,
        )

        return self.__parent__._cast(_4540.StraightBevelGearCompoundPowerFlow)

    @property
    def straight_bevel_planet_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4543.StraightBevelPlanetGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4543,
        )

        return self.__parent__._cast(_4543.StraightBevelPlanetGearCompoundPowerFlow)

    @property
    def straight_bevel_sun_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4544.StraightBevelSunGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4544,
        )

        return self.__parent__._cast(_4544.StraightBevelSunGearCompoundPowerFlow)

    @property
    def synchroniser_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4546.SynchroniserHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4546,
        )

        return self.__parent__._cast(_4546.SynchroniserHalfCompoundPowerFlow)

    @property
    def synchroniser_part_compound_power_flow(
        self: "CastSelf",
    ) -> "_4547.SynchroniserPartCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4547,
        )

        return self.__parent__._cast(_4547.SynchroniserPartCompoundPowerFlow)

    @property
    def synchroniser_sleeve_compound_power_flow(
        self: "CastSelf",
    ) -> "_4548.SynchroniserSleeveCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4548,
        )

        return self.__parent__._cast(_4548.SynchroniserSleeveCompoundPowerFlow)

    @property
    def torque_converter_pump_compound_power_flow(
        self: "CastSelf",
    ) -> "_4551.TorqueConverterPumpCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4551,
        )

        return self.__parent__._cast(_4551.TorqueConverterPumpCompoundPowerFlow)

    @property
    def torque_converter_turbine_compound_power_flow(
        self: "CastSelf",
    ) -> "_4552.TorqueConverterTurbineCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4552,
        )

        return self.__parent__._cast(_4552.TorqueConverterTurbineCompoundPowerFlow)

    @property
    def unbalanced_mass_compound_power_flow(
        self: "CastSelf",
    ) -> "_4553.UnbalancedMassCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4553,
        )

        return self.__parent__._cast(_4553.UnbalancedMassCompoundPowerFlow)

    @property
    def virtual_component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4554.VirtualComponentCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4554,
        )

        return self.__parent__._cast(_4554.VirtualComponentCompoundPowerFlow)

    @property
    def worm_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4555.WormGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4555,
        )

        return self.__parent__._cast(_4555.WormGearCompoundPowerFlow)

    @property
    def zerol_bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4558.ZerolBevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4558,
        )

        return self.__parent__._cast(_4558.ZerolBevelGearCompoundPowerFlow)

    @property
    def component_compound_power_flow(self: "CastSelf") -> "ComponentCompoundPowerFlow":
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
class ComponentCompoundPowerFlow(_4511.PartCompoundPowerFlow):
    """ComponentCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases(self: "Self") -> "List[_4318.ComponentPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.ComponentPowerFlow]

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
    ) -> "List[_4318.ComponentPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.ComponentPowerFlow]

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
    def cast_to(self: "Self") -> "_Cast_ComponentCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ComponentCompoundPowerFlow
        """
        return _Cast_ComponentCompoundPowerFlow(self)
