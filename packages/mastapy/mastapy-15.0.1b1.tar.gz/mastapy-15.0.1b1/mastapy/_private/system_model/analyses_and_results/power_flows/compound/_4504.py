"""KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4498,
)

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_POWER_FLOW = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
        "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4370
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4430,
        _4464,
        _4490,
        _4502,
        _4503,
        _4511,
        _4530,
    )
    from mastapy._private.system_model.part_model.gears import _2778

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow._Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow:
    """Special nested class for casting KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow to subclasses."""

    __parent__: "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4498.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow":
        return self.__parent__._cast(
            _4498.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow
        )

    @property
    def conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4464.ConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4464,
        )

        return self.__parent__._cast(_4464.ConicalGearSetCompoundPowerFlow)

    @property
    def gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4490.GearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4490,
        )

        return self.__parent__._cast(_4490.GearSetCompoundPowerFlow)

    @property
    def specialised_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4530.SpecialisedAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4530,
        )

        return self.__parent__._cast(_4530.SpecialisedAssemblyCompoundPowerFlow)

    @property
    def abstract_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4430.AbstractAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4430,
        )

        return self.__parent__._cast(_4430.AbstractAssemblyCompoundPowerFlow)

    @property
    def part_compound_power_flow(self: "CastSelf") -> "_4511.PartCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4511,
        )

        return self.__parent__._cast(_4511.PartCompoundPowerFlow)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7888.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7888,
        )

        return self.__parent__._cast(_7888.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7885.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7885,
        )

        return self.__parent__._cast(_7885.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow":
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
class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow(
    _4498.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow
):
    """KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_POWER_FLOW
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(
        self: "Self",
    ) -> "_2778.KlingelnbergCycloPalloidSpiralBevelGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet

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
    def assembly_design(
        self: "Self",
    ) -> "_2778.KlingelnbergCycloPalloidSpiralBevelGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet

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
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4370.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_power_flow(
        self: "Self",
    ) -> "List[_4502.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidSpiralBevelGearsCompoundPowerFlow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_power_flow(
        self: "Self",
    ) -> "List[_4503.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidSpiralBevelMeshesCompoundPowerFlow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_4370.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow
        """
        return _Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow(self)
