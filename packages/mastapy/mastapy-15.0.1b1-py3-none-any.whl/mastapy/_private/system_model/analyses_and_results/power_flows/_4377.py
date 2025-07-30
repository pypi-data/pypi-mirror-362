"""PartPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7890

_PART_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "PartPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7887
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4293,
        _4294,
        _4295,
        _4298,
        _4299,
        _4300,
        _4301,
        _4303,
        _4305,
        _4306,
        _4307,
        _4308,
        _4310,
        _4311,
        _4312,
        _4313,
        _4315,
        _4316,
        _4318,
        _4320,
        _4321,
        _4323,
        _4324,
        _4326,
        _4327,
        _4329,
        _4331,
        _4332,
        _4334,
        _4335,
        _4336,
        _4339,
        _4342,
        _4343,
        _4344,
        _4345,
        _4346,
        _4348,
        _4349,
        _4352,
        _4353,
        _4355,
        _4356,
        _4357,
        _4359,
        _4360,
        _4363,
        _4364,
        _4366,
        _4367,
        _4369,
        _4370,
        _4371,
        _4372,
        _4373,
        _4374,
        _4375,
        _4376,
        _4379,
        _4380,
        _4382,
        _4383,
        _4384,
        _4385,
        _4387,
        _4388,
        _4389,
        _4391,
        _4393,
        _4394,
        _4395,
        _4396,
        _4398,
        _4400,
        _4401,
        _4403,
        _4404,
        _4406,
        _4407,
        _4409,
        _4410,
        _4411,
        _4412,
        _4413,
        _4414,
        _4415,
        _4416,
        _4419,
        _4420,
        _4421,
        _4422,
        _4423,
        _4425,
        _4426,
        _4428,
        _4429,
    )
    from mastapy._private.system_model.drawing import _2475
    from mastapy._private.system_model.part_model import _2698

    Self = TypeVar("Self", bound="PartPowerFlow")
    CastSelf = TypeVar("CastSelf", bound="PartPowerFlow._Cast_PartPowerFlow")


__docformat__ = "restructuredtext en"
__all__ = ("PartPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartPowerFlow:
    """Special nested class for casting PartPowerFlow to subclasses."""

    __parent__: "PartPowerFlow"

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7890.PartStaticLoadAnalysisCase":
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
    def abstract_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4293.AbstractAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4293

        return self.__parent__._cast(_4293.AbstractAssemblyPowerFlow)

    @property
    def abstract_shaft_or_housing_power_flow(
        self: "CastSelf",
    ) -> "_4294.AbstractShaftOrHousingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4294

        return self.__parent__._cast(_4294.AbstractShaftOrHousingPowerFlow)

    @property
    def abstract_shaft_power_flow(self: "CastSelf") -> "_4295.AbstractShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4295

        return self.__parent__._cast(_4295.AbstractShaftPowerFlow)

    @property
    def agma_gleason_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4298.AGMAGleasonConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4298

        return self.__parent__._cast(_4298.AGMAGleasonConicalGearPowerFlow)

    @property
    def agma_gleason_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4299.AGMAGleasonConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4299

        return self.__parent__._cast(_4299.AGMAGleasonConicalGearSetPowerFlow)

    @property
    def assembly_power_flow(self: "CastSelf") -> "_4300.AssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4300

        return self.__parent__._cast(_4300.AssemblyPowerFlow)

    @property
    def bearing_power_flow(self: "CastSelf") -> "_4301.BearingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4301

        return self.__parent__._cast(_4301.BearingPowerFlow)

    @property
    def belt_drive_power_flow(self: "CastSelf") -> "_4303.BeltDrivePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4303

        return self.__parent__._cast(_4303.BeltDrivePowerFlow)

    @property
    def bevel_differential_gear_power_flow(
        self: "CastSelf",
    ) -> "_4305.BevelDifferentialGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4305

        return self.__parent__._cast(_4305.BevelDifferentialGearPowerFlow)

    @property
    def bevel_differential_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4306.BevelDifferentialGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4306

        return self.__parent__._cast(_4306.BevelDifferentialGearSetPowerFlow)

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
    def bevel_gear_set_power_flow(self: "CastSelf") -> "_4311.BevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4311

        return self.__parent__._cast(_4311.BevelGearSetPowerFlow)

    @property
    def bolted_joint_power_flow(self: "CastSelf") -> "_4312.BoltedJointPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4312

        return self.__parent__._cast(_4312.BoltedJointPowerFlow)

    @property
    def bolt_power_flow(self: "CastSelf") -> "_4313.BoltPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4313

        return self.__parent__._cast(_4313.BoltPowerFlow)

    @property
    def clutch_half_power_flow(self: "CastSelf") -> "_4315.ClutchHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4315

        return self.__parent__._cast(_4315.ClutchHalfPowerFlow)

    @property
    def clutch_power_flow(self: "CastSelf") -> "_4316.ClutchPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4316

        return self.__parent__._cast(_4316.ClutchPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4318.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4318

        return self.__parent__._cast(_4318.ComponentPowerFlow)

    @property
    def concept_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4320.ConceptCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4320

        return self.__parent__._cast(_4320.ConceptCouplingHalfPowerFlow)

    @property
    def concept_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4321.ConceptCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4321

        return self.__parent__._cast(_4321.ConceptCouplingPowerFlow)

    @property
    def concept_gear_power_flow(self: "CastSelf") -> "_4323.ConceptGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4323

        return self.__parent__._cast(_4323.ConceptGearPowerFlow)

    @property
    def concept_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4324.ConceptGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4324

        return self.__parent__._cast(_4324.ConceptGearSetPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "_4326.ConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4326

        return self.__parent__._cast(_4326.ConicalGearPowerFlow)

    @property
    def conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4327.ConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4327

        return self.__parent__._cast(_4327.ConicalGearSetPowerFlow)

    @property
    def connector_power_flow(self: "CastSelf") -> "_4329.ConnectorPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4329

        return self.__parent__._cast(_4329.ConnectorPowerFlow)

    @property
    def coupling_half_power_flow(self: "CastSelf") -> "_4331.CouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4331

        return self.__parent__._cast(_4331.CouplingHalfPowerFlow)

    @property
    def coupling_power_flow(self: "CastSelf") -> "_4332.CouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4332

        return self.__parent__._cast(_4332.CouplingPowerFlow)

    @property
    def cvt_power_flow(self: "CastSelf") -> "_4334.CVTPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4334

        return self.__parent__._cast(_4334.CVTPowerFlow)

    @property
    def cvt_pulley_power_flow(self: "CastSelf") -> "_4335.CVTPulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4335

        return self.__parent__._cast(_4335.CVTPulleyPowerFlow)

    @property
    def cycloidal_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4336.CycloidalAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4336

        return self.__parent__._cast(_4336.CycloidalAssemblyPowerFlow)

    @property
    def cycloidal_disc_power_flow(self: "CastSelf") -> "_4339.CycloidalDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4339

        return self.__parent__._cast(_4339.CycloidalDiscPowerFlow)

    @property
    def cylindrical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4342.CylindricalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4342

        return self.__parent__._cast(_4342.CylindricalGearPowerFlow)

    @property
    def cylindrical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4343.CylindricalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4343

        return self.__parent__._cast(_4343.CylindricalGearSetPowerFlow)

    @property
    def cylindrical_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4344.CylindricalPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4344

        return self.__parent__._cast(_4344.CylindricalPlanetGearPowerFlow)

    @property
    def datum_power_flow(self: "CastSelf") -> "_4345.DatumPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4345

        return self.__parent__._cast(_4345.DatumPowerFlow)

    @property
    def external_cad_model_power_flow(
        self: "CastSelf",
    ) -> "_4346.ExternalCADModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4346

        return self.__parent__._cast(_4346.ExternalCADModelPowerFlow)

    @property
    def face_gear_power_flow(self: "CastSelf") -> "_4348.FaceGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4348

        return self.__parent__._cast(_4348.FaceGearPowerFlow)

    @property
    def face_gear_set_power_flow(self: "CastSelf") -> "_4349.FaceGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4349

        return self.__parent__._cast(_4349.FaceGearSetPowerFlow)

    @property
    def fe_part_power_flow(self: "CastSelf") -> "_4352.FEPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4352

        return self.__parent__._cast(_4352.FEPartPowerFlow)

    @property
    def flexible_pin_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4353.FlexiblePinAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4353

        return self.__parent__._cast(_4353.FlexiblePinAssemblyPowerFlow)

    @property
    def gear_power_flow(self: "CastSelf") -> "_4355.GearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4355

        return self.__parent__._cast(_4355.GearPowerFlow)

    @property
    def gear_set_power_flow(self: "CastSelf") -> "_4356.GearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4356

        return self.__parent__._cast(_4356.GearSetPowerFlow)

    @property
    def guide_dxf_model_power_flow(self: "CastSelf") -> "_4357.GuideDxfModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4357

        return self.__parent__._cast(_4357.GuideDxfModelPowerFlow)

    @property
    def hypoid_gear_power_flow(self: "CastSelf") -> "_4359.HypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4359

        return self.__parent__._cast(_4359.HypoidGearPowerFlow)

    @property
    def hypoid_gear_set_power_flow(self: "CastSelf") -> "_4360.HypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4360

        return self.__parent__._cast(_4360.HypoidGearSetPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4363.KlingelnbergCycloPalloidConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4363

        return self.__parent__._cast(_4363.KlingelnbergCycloPalloidConicalGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4364.KlingelnbergCycloPalloidConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4364

        return self.__parent__._cast(
            _4364.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
        self: "CastSelf",
    ) -> "_4366.KlingelnbergCycloPalloidHypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4366

        return self.__parent__._cast(_4366.KlingelnbergCycloPalloidHypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4367.KlingelnbergCycloPalloidHypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4367

        return self.__parent__._cast(
            _4367.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4369.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4369

        return self.__parent__._cast(
            _4369.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4370.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4370

        return self.__parent__._cast(
            _4370.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
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
    def microphone_array_power_flow(
        self: "CastSelf",
    ) -> "_4373.MicrophoneArrayPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4373

        return self.__parent__._cast(_4373.MicrophoneArrayPowerFlow)

    @property
    def microphone_power_flow(self: "CastSelf") -> "_4374.MicrophonePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4374

        return self.__parent__._cast(_4374.MicrophonePowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4375.MountableComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4375

        return self.__parent__._cast(_4375.MountableComponentPowerFlow)

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
    def part_to_part_shear_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4380.PartToPartShearCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4380

        return self.__parent__._cast(_4380.PartToPartShearCouplingPowerFlow)

    @property
    def planetary_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4382.PlanetaryGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4382

        return self.__parent__._cast(_4382.PlanetaryGearSetPowerFlow)

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
    def rolling_ring_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4391.RollingRingAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4391

        return self.__parent__._cast(_4391.RollingRingAssemblyPowerFlow)

    @property
    def rolling_ring_power_flow(self: "CastSelf") -> "_4393.RollingRingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4393

        return self.__parent__._cast(_4393.RollingRingPowerFlow)

    @property
    def root_assembly_power_flow(self: "CastSelf") -> "_4394.RootAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4394

        return self.__parent__._cast(_4394.RootAssemblyPowerFlow)

    @property
    def shaft_hub_connection_power_flow(
        self: "CastSelf",
    ) -> "_4395.ShaftHubConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4395

        return self.__parent__._cast(_4395.ShaftHubConnectionPowerFlow)

    @property
    def shaft_power_flow(self: "CastSelf") -> "_4396.ShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4396

        return self.__parent__._cast(_4396.ShaftPowerFlow)

    @property
    def specialised_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4398.SpecialisedAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4398

        return self.__parent__._cast(_4398.SpecialisedAssemblyPowerFlow)

    @property
    def spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4400.SpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4400

        return self.__parent__._cast(_4400.SpiralBevelGearPowerFlow)

    @property
    def spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4401.SpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4401

        return self.__parent__._cast(_4401.SpiralBevelGearSetPowerFlow)

    @property
    def spring_damper_half_power_flow(
        self: "CastSelf",
    ) -> "_4403.SpringDamperHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4403

        return self.__parent__._cast(_4403.SpringDamperHalfPowerFlow)

    @property
    def spring_damper_power_flow(self: "CastSelf") -> "_4404.SpringDamperPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4404

        return self.__parent__._cast(_4404.SpringDamperPowerFlow)

    @property
    def straight_bevel_diff_gear_power_flow(
        self: "CastSelf",
    ) -> "_4406.StraightBevelDiffGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4406

        return self.__parent__._cast(_4406.StraightBevelDiffGearPowerFlow)

    @property
    def straight_bevel_diff_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4407.StraightBevelDiffGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4407

        return self.__parent__._cast(_4407.StraightBevelDiffGearSetPowerFlow)

    @property
    def straight_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4409.StraightBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4409

        return self.__parent__._cast(_4409.StraightBevelGearPowerFlow)

    @property
    def straight_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4410.StraightBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4410

        return self.__parent__._cast(_4410.StraightBevelGearSetPowerFlow)

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
    def synchroniser_power_flow(self: "CastSelf") -> "_4415.SynchroniserPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4415

        return self.__parent__._cast(_4415.SynchroniserPowerFlow)

    @property
    def synchroniser_sleeve_power_flow(
        self: "CastSelf",
    ) -> "_4416.SynchroniserSleevePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4416

        return self.__parent__._cast(_4416.SynchroniserSleevePowerFlow)

    @property
    def torque_converter_power_flow(
        self: "CastSelf",
    ) -> "_4419.TorqueConverterPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4419

        return self.__parent__._cast(_4419.TorqueConverterPowerFlow)

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
    def worm_gear_set_power_flow(self: "CastSelf") -> "_4426.WormGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4426

        return self.__parent__._cast(_4426.WormGearSetPowerFlow)

    @property
    def zerol_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4428.ZerolBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4428

        return self.__parent__._cast(_4428.ZerolBevelGearPowerFlow)

    @property
    def zerol_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4429.ZerolBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4429

        return self.__parent__._cast(_4429.ZerolBevelGearSetPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "PartPowerFlow":
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
class PartPowerFlow(_7890.PartStaticLoadAnalysisCase):
    """PartPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def two_d_drawing_showing_power_flow(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawingShowingPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2698.Part":
        """mastapy.system_model.part_model.Part

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
    def power_flow(self: "Self") -> "_4385.PowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.PowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlow")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def create_viewable(self: "Self") -> "_2475.PowerFlowViewable":
        """mastapy.system_model.drawing.PowerFlowViewable"""
        method_result = pythonnet_method_call(self.wrapped, "CreateViewable")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_PartPowerFlow
        """
        return _Cast_PartPowerFlow(self)
