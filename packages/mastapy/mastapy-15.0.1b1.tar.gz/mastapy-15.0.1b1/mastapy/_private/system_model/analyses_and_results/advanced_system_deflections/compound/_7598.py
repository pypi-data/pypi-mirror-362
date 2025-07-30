"""KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7564,
)

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7465,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7530,
        _7590,
        _7601,
        _7604,
        _7611,
        _7630,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )

    Self = TypeVar(
        "Self",
        bound="KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection"

    @property
    def conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7564.ConicalGearSetCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(
            _7564.ConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7590.GearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7590,
        )

        return self.__parent__._cast(_7590.GearSetCompoundAdvancedSystemDeflection)

    @property
    def specialised_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7630.SpecialisedAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7630,
        )

        return self.__parent__._cast(
            _7630.SpecialisedAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def abstract_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7530.AbstractAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7530,
        )

        return self.__parent__._cast(
            _7530.AbstractAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7611.PartCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7611,
        )

        return self.__parent__._cast(_7611.PartCompoundAdvancedSystemDeflection)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7601.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7601,
        )

        return self.__parent__._cast(
            _7601.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7604.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7604,
        )

        return self.__parent__._cast(
            _7604.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection":
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
class KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection(
    _7564.ConicalGearSetCompoundAdvancedSystemDeflection
):
    """KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_7465.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection]

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
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_7465.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection(
            self
        )
