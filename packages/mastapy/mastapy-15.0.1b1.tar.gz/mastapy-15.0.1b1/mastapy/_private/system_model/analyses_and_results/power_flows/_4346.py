"""ExternalCADModelPowerFlow"""

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

_EXTERNAL_CAD_MODEL_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "ExternalCADModelPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4377
    from mastapy._private.system_model.analyses_and_results.static_loads import _7752
    from mastapy._private.system_model.part_model import _2679

    Self = TypeVar("Self", bound="ExternalCADModelPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="ExternalCADModelPowerFlow._Cast_ExternalCADModelPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExternalCADModelPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExternalCADModelPowerFlow:
    """Special nested class for casting ExternalCADModelPowerFlow to subclasses."""

    __parent__: "ExternalCADModelPowerFlow"

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
    def external_cad_model_power_flow(self: "CastSelf") -> "ExternalCADModelPowerFlow":
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
class ExternalCADModelPowerFlow(_4318.ComponentPowerFlow):
    """ExternalCADModelPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXTERNAL_CAD_MODEL_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def component_design(self: "Self") -> "_2679.ExternalCADModel":
        """mastapy.system_model.part_model.ExternalCADModel

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
    def component_load_case(self: "Self") -> "_7752.ExternalCADModelLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ExternalCADModelPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ExternalCADModelPowerFlow
        """
        return _Cast_ExternalCADModelPowerFlow(self)
