"""AbstractAssemblyPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows import _4377

_ABSTRACT_ASSEMBLY_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "AbstractAssemblyPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4299,
        _4300,
        _4303,
        _4306,
        _4311,
        _4312,
        _4316,
        _4321,
        _4324,
        _4327,
        _4332,
        _4334,
        _4336,
        _4343,
        _4349,
        _4353,
        _4356,
        _4360,
        _4364,
        _4367,
        _4370,
        _4373,
        _4380,
        _4382,
        _4391,
        _4394,
        _4398,
        _4401,
        _4404,
        _4407,
        _4410,
        _4415,
        _4419,
        _4426,
        _4429,
    )
    from mastapy._private.system_model.part_model import _2659

    Self = TypeVar("Self", bound="AbstractAssemblyPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyPowerFlow:
    """Special nested class for casting AbstractAssemblyPowerFlow to subclasses."""

    __parent__: "AbstractAssemblyPowerFlow"

    @property
    def part_power_flow(self: "CastSelf") -> "_4377.PartPowerFlow":
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
    def belt_drive_power_flow(self: "CastSelf") -> "_4303.BeltDrivePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4303

        return self.__parent__._cast(_4303.BeltDrivePowerFlow)

    @property
    def bevel_differential_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4306.BevelDifferentialGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4306

        return self.__parent__._cast(_4306.BevelDifferentialGearSetPowerFlow)

    @property
    def bevel_gear_set_power_flow(self: "CastSelf") -> "_4311.BevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4311

        return self.__parent__._cast(_4311.BevelGearSetPowerFlow)

    @property
    def bolted_joint_power_flow(self: "CastSelf") -> "_4312.BoltedJointPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4312

        return self.__parent__._cast(_4312.BoltedJointPowerFlow)

    @property
    def clutch_power_flow(self: "CastSelf") -> "_4316.ClutchPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4316

        return self.__parent__._cast(_4316.ClutchPowerFlow)

    @property
    def concept_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4321.ConceptCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4321

        return self.__parent__._cast(_4321.ConceptCouplingPowerFlow)

    @property
    def concept_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4324.ConceptGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4324

        return self.__parent__._cast(_4324.ConceptGearSetPowerFlow)

    @property
    def conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4327.ConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4327

        return self.__parent__._cast(_4327.ConicalGearSetPowerFlow)

    @property
    def coupling_power_flow(self: "CastSelf") -> "_4332.CouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4332

        return self.__parent__._cast(_4332.CouplingPowerFlow)

    @property
    def cvt_power_flow(self: "CastSelf") -> "_4334.CVTPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4334

        return self.__parent__._cast(_4334.CVTPowerFlow)

    @property
    def cycloidal_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4336.CycloidalAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4336

        return self.__parent__._cast(_4336.CycloidalAssemblyPowerFlow)

    @property
    def cylindrical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4343.CylindricalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4343

        return self.__parent__._cast(_4343.CylindricalGearSetPowerFlow)

    @property
    def face_gear_set_power_flow(self: "CastSelf") -> "_4349.FaceGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4349

        return self.__parent__._cast(_4349.FaceGearSetPowerFlow)

    @property
    def flexible_pin_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4353.FlexiblePinAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4353

        return self.__parent__._cast(_4353.FlexiblePinAssemblyPowerFlow)

    @property
    def gear_set_power_flow(self: "CastSelf") -> "_4356.GearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4356

        return self.__parent__._cast(_4356.GearSetPowerFlow)

    @property
    def hypoid_gear_set_power_flow(self: "CastSelf") -> "_4360.HypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4360

        return self.__parent__._cast(_4360.HypoidGearSetPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4364.KlingelnbergCycloPalloidConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4364

        return self.__parent__._cast(
            _4364.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4367.KlingelnbergCycloPalloidHypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4367

        return self.__parent__._cast(
            _4367.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
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
    def microphone_array_power_flow(
        self: "CastSelf",
    ) -> "_4373.MicrophoneArrayPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4373

        return self.__parent__._cast(_4373.MicrophoneArrayPowerFlow)

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
    def rolling_ring_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4391.RollingRingAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4391

        return self.__parent__._cast(_4391.RollingRingAssemblyPowerFlow)

    @property
    def root_assembly_power_flow(self: "CastSelf") -> "_4394.RootAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4394

        return self.__parent__._cast(_4394.RootAssemblyPowerFlow)

    @property
    def specialised_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4398.SpecialisedAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4398

        return self.__parent__._cast(_4398.SpecialisedAssemblyPowerFlow)

    @property
    def spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4401.SpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4401

        return self.__parent__._cast(_4401.SpiralBevelGearSetPowerFlow)

    @property
    def spring_damper_power_flow(self: "CastSelf") -> "_4404.SpringDamperPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4404

        return self.__parent__._cast(_4404.SpringDamperPowerFlow)

    @property
    def straight_bevel_diff_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4407.StraightBevelDiffGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4407

        return self.__parent__._cast(_4407.StraightBevelDiffGearSetPowerFlow)

    @property
    def straight_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4410.StraightBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4410

        return self.__parent__._cast(_4410.StraightBevelGearSetPowerFlow)

    @property
    def synchroniser_power_flow(self: "CastSelf") -> "_4415.SynchroniserPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4415

        return self.__parent__._cast(_4415.SynchroniserPowerFlow)

    @property
    def torque_converter_power_flow(
        self: "CastSelf",
    ) -> "_4419.TorqueConverterPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4419

        return self.__parent__._cast(_4419.TorqueConverterPowerFlow)

    @property
    def worm_gear_set_power_flow(self: "CastSelf") -> "_4426.WormGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4426

        return self.__parent__._cast(_4426.WormGearSetPowerFlow)

    @property
    def zerol_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4429.ZerolBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4429

        return self.__parent__._cast(_4429.ZerolBevelGearSetPowerFlow)

    @property
    def abstract_assembly_power_flow(self: "CastSelf") -> "AbstractAssemblyPowerFlow":
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
class AbstractAssemblyPowerFlow(_4377.PartPowerFlow):
    """AbstractAssemblyPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2659.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

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
    def assembly_design(self: "Self") -> "_2659.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyPowerFlow
        """
        return _Cast_AbstractAssemblyPowerFlow(self)
