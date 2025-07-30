"""WormGearSetPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows import _4356

_WORM_GEAR_SET_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "WormGearSetPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.worm import _467
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4293,
        _4377,
        _4398,
        _4424,
        _4425,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7856
    from mastapy._private.system_model.part_model.gears import _2790

    Self = TypeVar("Self", bound="WormGearSetPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="WormGearSetPowerFlow._Cast_WormGearSetPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGearSetPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearSetPowerFlow:
    """Special nested class for casting WormGearSetPowerFlow to subclasses."""

    __parent__: "WormGearSetPowerFlow"

    @property
    def gear_set_power_flow(self: "CastSelf") -> "_4356.GearSetPowerFlow":
        return self.__parent__._cast(_4356.GearSetPowerFlow)

    @property
    def specialised_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4398.SpecialisedAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4398

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
    def worm_gear_set_power_flow(self: "CastSelf") -> "WormGearSetPowerFlow":
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
class WormGearSetPowerFlow(_4356.GearSetPowerFlow):
    """WormGearSetPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_SET_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2790.WormGearSet":
        """mastapy.system_model.part_model.gears.WormGearSet

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
    def assembly_load_case(self: "Self") -> "_7856.WormGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rating(self: "Self") -> "_467.WormGearSetRating":
        """mastapy.gears.rating.worm.WormGearSetRating

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
    def component_detailed_analysis(self: "Self") -> "_467.WormGearSetRating":
        """mastapy.gears.rating.worm.WormGearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gears_power_flow(self: "Self") -> "List[_4425.WormGearPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.WormGearPowerFlow]

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
    def worm_gears_power_flow(self: "Self") -> "List[_4425.WormGearPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.WormGearPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearsPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes_power_flow(self: "Self") -> "List[_4424.WormGearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.WormGearMeshPowerFlow]

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

    @property
    @exception_bridge
    def worm_meshes_power_flow(self: "Self") -> "List[_4424.WormGearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.WormGearMeshPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormMeshesPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearSetPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_WormGearSetPowerFlow
        """
        return _Cast_WormGearSetPowerFlow(self)
