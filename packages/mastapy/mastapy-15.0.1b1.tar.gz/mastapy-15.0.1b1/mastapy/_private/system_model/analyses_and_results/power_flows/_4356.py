"""GearSetPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4398

_GEAR_SET_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "GearSetPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating import _454
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4293,
        _4299,
        _4306,
        _4311,
        _4324,
        _4327,
        _4343,
        _4349,
        _4354,
        _4355,
        _4360,
        _4364,
        _4367,
        _4370,
        _4377,
        _4382,
        _4401,
        _4407,
        _4410,
        _4426,
        _4429,
    )
    from mastapy._private.system_model.part_model.gears import _2769

    Self = TypeVar("Self", bound="GearSetPowerFlow")
    CastSelf = TypeVar("CastSelf", bound="GearSetPowerFlow._Cast_GearSetPowerFlow")


__docformat__ = "restructuredtext en"
__all__ = ("GearSetPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetPowerFlow:
    """Special nested class for casting GearSetPowerFlow to subclasses."""

    __parent__: "GearSetPowerFlow"

    @property
    def specialised_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4398.SpecialisedAssemblyPowerFlow":
        return self.__parent__._cast(_4398.SpecialisedAssemblyPowerFlow)

    @property
    def abstract_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4293.AbstractAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4293

        return self.__parent__._cast(_4293.AbstractAssemblyPowerFlow)

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
    def agma_gleason_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4299.AGMAGleasonConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4299

        return self.__parent__._cast(_4299.AGMAGleasonConicalGearSetPowerFlow)

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
    def planetary_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4382.PlanetaryGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4382

        return self.__parent__._cast(_4382.PlanetaryGearSetPowerFlow)

    @property
    def spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4401.SpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4401

        return self.__parent__._cast(_4401.SpiralBevelGearSetPowerFlow)

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
    def gear_set_power_flow(self: "CastSelf") -> "GearSetPowerFlow":
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
class GearSetPowerFlow(_4398.SpecialisedAssemblyPowerFlow):
    """GearSetPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2769.GearSet":
        """mastapy.system_model.part_model.gears.GearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rating(self: "Self") -> "_454.GearSetRating":
        """mastapy.gears.rating.GearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gears_power_flow(self: "Self") -> "List[_4355.GearPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.GearPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes_power_flow(self: "Self") -> "List[_4354.GearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.GearMeshPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def set_face_widths_for_specified_safety_factors(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetFaceWidthsForSpecifiedSafetyFactors")

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_GearSetPowerFlow
        """
        return _Cast_GearSetPowerFlow(self)
