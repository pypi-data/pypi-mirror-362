"""ConceptGearSetPowerFlow"""

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

_CONCEPT_GEAR_SET_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "ConceptGearSetPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.concept import _644
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4293,
        _4322,
        _4323,
        _4377,
        _4398,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7712
    from mastapy._private.system_model.part_model.gears import _2759

    Self = TypeVar("Self", bound="ConceptGearSetPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="ConceptGearSetPowerFlow._Cast_ConceptGearSetPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearSetPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearSetPowerFlow:
    """Special nested class for casting ConceptGearSetPowerFlow to subclasses."""

    __parent__: "ConceptGearSetPowerFlow"

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
    def concept_gear_set_power_flow(self: "CastSelf") -> "ConceptGearSetPowerFlow":
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
class ConceptGearSetPowerFlow(_4356.GearSetPowerFlow):
    """ConceptGearSetPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_SET_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2759.ConceptGearSet":
        """mastapy.system_model.part_model.gears.ConceptGearSet

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
    def assembly_load_case(self: "Self") -> "_7712.ConceptGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase

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
    def rating(self: "Self") -> "_644.ConceptGearSetRating":
        """mastapy.gears.rating.concept.ConceptGearSetRating

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
    def component_detailed_analysis(self: "Self") -> "_644.ConceptGearSetRating":
        """mastapy.gears.rating.concept.ConceptGearSetRating

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
    def gears_power_flow(self: "Self") -> "List[_4323.ConceptGearPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.ConceptGearPowerFlow]

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
    def concept_gears_power_flow(self: "Self") -> "List[_4323.ConceptGearPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.ConceptGearPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptGearsPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes_power_flow(self: "Self") -> "List[_4322.ConceptGearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.ConceptGearMeshPowerFlow]

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
    def concept_meshes_power_flow(
        self: "Self",
    ) -> "List[_4322.ConceptGearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.ConceptGearMeshPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptMeshesPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptGearSetPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearSetPowerFlow
        """
        return _Cast_ConceptGearSetPowerFlow(self)
