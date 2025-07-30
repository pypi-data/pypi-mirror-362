"""MountableComponentPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4318

_MOUNTABLE_COMPONENT_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "MountableComponentPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4298,
        _4301,
        _4305,
        _4307,
        _4308,
        _4310,
        _4315,
        _4320,
        _4323,
        _4326,
        _4329,
        _4331,
        _4335,
        _4342,
        _4344,
        _4348,
        _4355,
        _4359,
        _4363,
        _4366,
        _4369,
        _4371,
        _4372,
        _4376,
        _4377,
        _4379,
        _4383,
        _4384,
        _4387,
        _4388,
        _4389,
        _4393,
        _4395,
        _4400,
        _4403,
        _4406,
        _4409,
        _4411,
        _4412,
        _4413,
        _4414,
        _4416,
        _4420,
        _4421,
        _4422,
        _4423,
        _4425,
        _4428,
    )
    from mastapy._private.system_model.part_model import _2693

    Self = TypeVar("Self", bound="MountableComponentPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentPowerFlow:
    """Special nested class for casting MountableComponentPowerFlow to subclasses."""

    __parent__: "MountableComponentPowerFlow"

    @property
    def component_power_flow(self: "CastSelf") -> "_4318.ComponentPowerFlow":
        return self.__parent__._cast(_4318.ComponentPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "_4377.PartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4377

        return self.__parent__._cast(_4377.PartPowerFlow)

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
    def agma_gleason_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4298.AGMAGleasonConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4298

        return self.__parent__._cast(_4298.AGMAGleasonConicalGearPowerFlow)

    @property
    def bearing_power_flow(self: "CastSelf") -> "_4301.BearingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4301

        return self.__parent__._cast(_4301.BearingPowerFlow)

    @property
    def bevel_differential_gear_power_flow(
        self: "CastSelf",
    ) -> "_4305.BevelDifferentialGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4305

        return self.__parent__._cast(_4305.BevelDifferentialGearPowerFlow)

    @property
    def bevel_differential_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4307.BevelDifferentialPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4307

        return self.__parent__._cast(_4307.BevelDifferentialPlanetGearPowerFlow)

    @property
    def bevel_differential_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4308.BevelDifferentialSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4308

        return self.__parent__._cast(_4308.BevelDifferentialSunGearPowerFlow)

    @property
    def bevel_gear_power_flow(self: "CastSelf") -> "_4310.BevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4310

        return self.__parent__._cast(_4310.BevelGearPowerFlow)

    @property
    def clutch_half_power_flow(self: "CastSelf") -> "_4315.ClutchHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4315

        return self.__parent__._cast(_4315.ClutchHalfPowerFlow)

    @property
    def concept_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4320.ConceptCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4320

        return self.__parent__._cast(_4320.ConceptCouplingHalfPowerFlow)

    @property
    def concept_gear_power_flow(self: "CastSelf") -> "_4323.ConceptGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4323

        return self.__parent__._cast(_4323.ConceptGearPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "_4326.ConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4326

        return self.__parent__._cast(_4326.ConicalGearPowerFlow)

    @property
    def connector_power_flow(self: "CastSelf") -> "_4329.ConnectorPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4329

        return self.__parent__._cast(_4329.ConnectorPowerFlow)

    @property
    def coupling_half_power_flow(self: "CastSelf") -> "_4331.CouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4331

        return self.__parent__._cast(_4331.CouplingHalfPowerFlow)

    @property
    def cvt_pulley_power_flow(self: "CastSelf") -> "_4335.CVTPulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4335

        return self.__parent__._cast(_4335.CVTPulleyPowerFlow)

    @property
    def cylindrical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4342.CylindricalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4342

        return self.__parent__._cast(_4342.CylindricalGearPowerFlow)

    @property
    def cylindrical_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4344.CylindricalPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4344

        return self.__parent__._cast(_4344.CylindricalPlanetGearPowerFlow)

    @property
    def face_gear_power_flow(self: "CastSelf") -> "_4348.FaceGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4348

        return self.__parent__._cast(_4348.FaceGearPowerFlow)

    @property
    def gear_power_flow(self: "CastSelf") -> "_4355.GearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4355

        return self.__parent__._cast(_4355.GearPowerFlow)

    @property
    def hypoid_gear_power_flow(self: "CastSelf") -> "_4359.HypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4359

        return self.__parent__._cast(_4359.HypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4363.KlingelnbergCycloPalloidConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4363

        return self.__parent__._cast(_4363.KlingelnbergCycloPalloidConicalGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
        self: "CastSelf",
    ) -> "_4366.KlingelnbergCycloPalloidHypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4366

        return self.__parent__._cast(_4366.KlingelnbergCycloPalloidHypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4369.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4369

        return self.__parent__._cast(
            _4369.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        )

    @property
    def mass_disc_power_flow(self: "CastSelf") -> "_4371.MassDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4371

        return self.__parent__._cast(_4371.MassDiscPowerFlow)

    @property
    def measurement_component_power_flow(
        self: "CastSelf",
    ) -> "_4372.MeasurementComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4372

        return self.__parent__._cast(_4372.MeasurementComponentPowerFlow)

    @property
    def oil_seal_power_flow(self: "CastSelf") -> "_4376.OilSealPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4376

        return self.__parent__._cast(_4376.OilSealPowerFlow)

    @property
    def part_to_part_shear_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4379.PartToPartShearCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4379

        return self.__parent__._cast(_4379.PartToPartShearCouplingHalfPowerFlow)

    @property
    def planet_carrier_power_flow(self: "CastSelf") -> "_4383.PlanetCarrierPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4383

        return self.__parent__._cast(_4383.PlanetCarrierPowerFlow)

    @property
    def point_load_power_flow(self: "CastSelf") -> "_4384.PointLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4384

        return self.__parent__._cast(_4384.PointLoadPowerFlow)

    @property
    def power_load_power_flow(self: "CastSelf") -> "_4387.PowerLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4387

        return self.__parent__._cast(_4387.PowerLoadPowerFlow)

    @property
    def pulley_power_flow(self: "CastSelf") -> "_4388.PulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4388

        return self.__parent__._cast(_4388.PulleyPowerFlow)

    @property
    def ring_pins_power_flow(self: "CastSelf") -> "_4389.RingPinsPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4389

        return self.__parent__._cast(_4389.RingPinsPowerFlow)

    @property
    def rolling_ring_power_flow(self: "CastSelf") -> "_4393.RollingRingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4393

        return self.__parent__._cast(_4393.RollingRingPowerFlow)

    @property
    def shaft_hub_connection_power_flow(
        self: "CastSelf",
    ) -> "_4395.ShaftHubConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4395

        return self.__parent__._cast(_4395.ShaftHubConnectionPowerFlow)

    @property
    def spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4400.SpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4400

        return self.__parent__._cast(_4400.SpiralBevelGearPowerFlow)

    @property
    def spring_damper_half_power_flow(
        self: "CastSelf",
    ) -> "_4403.SpringDamperHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4403

        return self.__parent__._cast(_4403.SpringDamperHalfPowerFlow)

    @property
    def straight_bevel_diff_gear_power_flow(
        self: "CastSelf",
    ) -> "_4406.StraightBevelDiffGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4406

        return self.__parent__._cast(_4406.StraightBevelDiffGearPowerFlow)

    @property
    def straight_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4409.StraightBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4409

        return self.__parent__._cast(_4409.StraightBevelGearPowerFlow)

    @property
    def straight_bevel_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4411.StraightBevelPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4411

        return self.__parent__._cast(_4411.StraightBevelPlanetGearPowerFlow)

    @property
    def straight_bevel_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4412.StraightBevelSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4412

        return self.__parent__._cast(_4412.StraightBevelSunGearPowerFlow)

    @property
    def synchroniser_half_power_flow(
        self: "CastSelf",
    ) -> "_4413.SynchroniserHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4413

        return self.__parent__._cast(_4413.SynchroniserHalfPowerFlow)

    @property
    def synchroniser_part_power_flow(
        self: "CastSelf",
    ) -> "_4414.SynchroniserPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4414

        return self.__parent__._cast(_4414.SynchroniserPartPowerFlow)

    @property
    def synchroniser_sleeve_power_flow(
        self: "CastSelf",
    ) -> "_4416.SynchroniserSleevePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4416

        return self.__parent__._cast(_4416.SynchroniserSleevePowerFlow)

    @property
    def torque_converter_pump_power_flow(
        self: "CastSelf",
    ) -> "_4420.TorqueConverterPumpPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4420

        return self.__parent__._cast(_4420.TorqueConverterPumpPowerFlow)

    @property
    def torque_converter_turbine_power_flow(
        self: "CastSelf",
    ) -> "_4421.TorqueConverterTurbinePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4421

        return self.__parent__._cast(_4421.TorqueConverterTurbinePowerFlow)

    @property
    def unbalanced_mass_power_flow(self: "CastSelf") -> "_4422.UnbalancedMassPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4422

        return self.__parent__._cast(_4422.UnbalancedMassPowerFlow)

    @property
    def virtual_component_power_flow(
        self: "CastSelf",
    ) -> "_4423.VirtualComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4423

        return self.__parent__._cast(_4423.VirtualComponentPowerFlow)

    @property
    def worm_gear_power_flow(self: "CastSelf") -> "_4425.WormGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4425

        return self.__parent__._cast(_4425.WormGearPowerFlow)

    @property
    def zerol_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4428.ZerolBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4428

        return self.__parent__._cast(_4428.ZerolBevelGearPowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "MountableComponentPowerFlow":
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
class MountableComponentPowerFlow(_4318.ComponentPowerFlow):
    """MountableComponentPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2693.MountableComponent":
        """mastapy.system_model.part_model.MountableComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponentPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentPowerFlow
        """
        return _Cast_MountableComponentPowerFlow(self)
