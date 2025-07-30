"""StraightBevelDiffGearPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows import _4310

_STRAIGHT_BEVEL_DIFF_GEAR_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "StraightBevelDiffGearPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.straight_bevel_diff import _490
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4298,
        _4318,
        _4326,
        _4355,
        _4375,
        _4377,
        _4411,
        _4412,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7830
    from mastapy._private.system_model.part_model.gears import _2783

    Self = TypeVar("Self", bound="StraightBevelDiffGearPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearPowerFlow._Cast_StraightBevelDiffGearPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearPowerFlow:
    """Special nested class for casting StraightBevelDiffGearPowerFlow to subclasses."""

    __parent__: "StraightBevelDiffGearPowerFlow"

    @property
    def bevel_gear_power_flow(self: "CastSelf") -> "_4310.BevelGearPowerFlow":
        return self.__parent__._cast(_4310.BevelGearPowerFlow)

    @property
    def agma_gleason_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4298.AGMAGleasonConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4298

        return self.__parent__._cast(_4298.AGMAGleasonConicalGearPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "_4326.ConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4326

        return self.__parent__._cast(_4326.ConicalGearPowerFlow)

    @property
    def gear_power_flow(self: "CastSelf") -> "_4355.GearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4355

        return self.__parent__._cast(_4355.GearPowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4375.MountableComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4375

        return self.__parent__._cast(_4375.MountableComponentPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4318.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4318

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
    def straight_bevel_diff_gear_power_flow(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearPowerFlow":
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
class StraightBevelDiffGearPowerFlow(_4310.BevelGearPowerFlow):
    """StraightBevelDiffGearPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2783.StraightBevelDiffGear":
        """mastapy.system_model.part_model.gears.StraightBevelDiffGear

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
    def component_detailed_analysis(self: "Self") -> "_490.StraightBevelDiffGearRating":
        """mastapy.gears.rating.straight_bevel_diff.StraightBevelDiffGearRating

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
    def component_load_case(self: "Self") -> "_7830.StraightBevelDiffGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGearPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearPowerFlow
        """
        return _Cast_StraightBevelDiffGearPowerFlow(self)
