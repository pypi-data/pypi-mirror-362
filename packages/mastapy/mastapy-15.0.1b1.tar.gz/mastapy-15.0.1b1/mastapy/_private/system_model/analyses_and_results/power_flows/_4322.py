"""ConceptGearMeshPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows import _4354

_CONCEPT_GEAR_MESH_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "ConceptGearMeshPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.concept import _641
    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4328,
        _4361,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7711
    from mastapy._private.system_model.connections_and_sockets.gears import _2526

    Self = TypeVar("Self", bound="ConceptGearMeshPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="ConceptGearMeshPowerFlow._Cast_ConceptGearMeshPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearMeshPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearMeshPowerFlow:
    """Special nested class for casting ConceptGearMeshPowerFlow to subclasses."""

    __parent__: "ConceptGearMeshPowerFlow"

    @property
    def gear_mesh_power_flow(self: "CastSelf") -> "_4354.GearMeshPowerFlow":
        return self.__parent__._cast(_4354.GearMeshPowerFlow)

    @property
    def inter_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4361.InterMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4361

        return self.__parent__._cast(_4361.InterMountableComponentConnectionPowerFlow)

    @property
    def connection_power_flow(self: "CastSelf") -> "_4328.ConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4328

        return self.__parent__._cast(_4328.ConnectionPowerFlow)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7883.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7883,
        )

        return self.__parent__._cast(_7883.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7880.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7880,
        )

        return self.__parent__._cast(_7880.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2890.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.ConnectionAnalysis)

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
    def concept_gear_mesh_power_flow(self: "CastSelf") -> "ConceptGearMeshPowerFlow":
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
class ConceptGearMeshPowerFlow(_4354.GearMeshPowerFlow):
    """ConceptGearMeshPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_MESH_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def rating(self: "Self") -> "_641.ConceptGearMeshRating":
        """mastapy.gears.rating.concept.ConceptGearMeshRating

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
    def component_detailed_analysis(self: "Self") -> "_641.ConceptGearMeshRating":
        """mastapy.gears.rating.concept.ConceptGearMeshRating

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
    def connection_design(self: "Self") -> "_2526.ConceptGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_load_case(self: "Self") -> "_7711.ConceptGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptGearMeshPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearMeshPowerFlow
        """
        return _Cast_ConceptGearMeshPowerFlow(self)
