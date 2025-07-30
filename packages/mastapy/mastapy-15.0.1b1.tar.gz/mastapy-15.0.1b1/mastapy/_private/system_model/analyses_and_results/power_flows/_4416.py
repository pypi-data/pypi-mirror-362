"""SynchroniserSleevePowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows import _4414

_SYNCHRONISER_SLEEVE_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "SynchroniserSleevePowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4318,
        _4331,
        _4375,
        _4377,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7841
    from mastapy._private.system_model.part_model.couplings import _2852

    Self = TypeVar("Self", bound="SynchroniserSleevePowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SynchroniserSleevePowerFlow._Cast_SynchroniserSleevePowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserSleevePowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SynchroniserSleevePowerFlow:
    """Special nested class for casting SynchroniserSleevePowerFlow to subclasses."""

    __parent__: "SynchroniserSleevePowerFlow"

    @property
    def synchroniser_part_power_flow(
        self: "CastSelf",
    ) -> "_4414.SynchroniserPartPowerFlow":
        return self.__parent__._cast(_4414.SynchroniserPartPowerFlow)

    @property
    def coupling_half_power_flow(self: "CastSelf") -> "_4331.CouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4331

        return self.__parent__._cast(_4331.CouplingHalfPowerFlow)

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
    def synchroniser_sleeve_power_flow(
        self: "CastSelf",
    ) -> "SynchroniserSleevePowerFlow":
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
class SynchroniserSleevePowerFlow(_4414.SynchroniserPartPowerFlow):
    """SynchroniserSleevePowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYNCHRONISER_SLEEVE_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2852.SynchroniserSleeve":
        """mastapy.system_model.part_model.couplings.SynchroniserSleeve

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
    def component_load_case(self: "Self") -> "_7841.SynchroniserSleeveLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SynchroniserSleevePowerFlow":
        """Cast to another type.

        Returns:
            _Cast_SynchroniserSleevePowerFlow
        """
        return _Cast_SynchroniserSleevePowerFlow(self)
