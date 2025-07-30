"""KlingelnbergCycloPalloidConicalGearSetSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.system_deflections import _2966

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "KlingelnbergCycloPalloidConicalGearSetSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7889,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4364
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2926,
        _3001,
        _3009,
        _3011,
        _3013,
        _3016,
        _3028,
        _3049,
    )
    from mastapy._private.system_model.part_model.gears import _2774

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidConicalGearSetSystemDeflection"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearSetSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearSetSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearSetSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearSetSystemDeflection:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearSetSystemDeflection to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearSetSystemDeflection"

    @property
    def conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2966.ConicalGearSetSystemDeflection":
        return self.__parent__._cast(_2966.ConicalGearSetSystemDeflection)

    @property
    def gear_set_system_deflection(self: "CastSelf") -> "_3001.GearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3001,
        )

        return self.__parent__._cast(_3001.GearSetSystemDeflection)

    @property
    def specialised_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_3049.SpecialisedAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3049,
        )

        return self.__parent__._cast(_3049.SpecialisedAssemblySystemDeflection)

    @property
    def abstract_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2926.AbstractAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2926,
        )

        return self.__parent__._cast(_2926.AbstractAssemblySystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_3028.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3028,
        )

        return self.__parent__._cast(_3028.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7889.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7889,
        )

        return self.__parent__._cast(_7889.PartFEAnalysis)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3013.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3013,
        )

        return self.__parent__._cast(
            _3013.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3016.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3016,
        )

        return self.__parent__._cast(
            _3016.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearSetSystemDeflection":
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
class KlingelnbergCycloPalloidConicalGearSetSystemDeflection(
    _2966.ConicalGearSetSystemDeflection
):
    """KlingelnbergCycloPalloidConicalGearSetSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_SYSTEM_DEFLECTION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2774.KlingelnbergCycloPalloidConicalGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet

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
    def conical_gears_system_deflection(
        self: "Self",
    ) -> "List[_3011.KlingelnbergCycloPalloidConicalGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidConicalGearSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearsSystemDeflection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_conical_gears_system_deflection(
        self: "Self",
    ) -> "List[_3011.KlingelnbergCycloPalloidConicalGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidConicalGearSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidConicalGearsSystemDeflection"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def conical_meshes_system_deflection(
        self: "Self",
    ) -> "List[_3009.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshesSystemDeflection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_conical_meshes_system_deflection(
        self: "Self",
    ) -> "List[_3009.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidConicalMeshesSystemDeflection"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def power_flow_results(
        self: "Self",
    ) -> "_4364.KlingelnbergCycloPalloidConicalGearSetPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearSetPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearSetSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearSetSystemDeflection
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearSetSystemDeflection(self)
