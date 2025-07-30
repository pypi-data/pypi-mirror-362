"""ConicalGearSetCompoundSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _3155,
)

_CONICAL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "ConicalGearSetCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.conical import _632
    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2966,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3094,
        _3100,
        _3107,
        _3112,
        _3159,
        _3163,
        _3166,
        _3169,
        _3176,
        _3196,
        _3199,
        _3205,
        _3208,
        _3226,
    )

    Self = TypeVar("Self", bound="ConicalGearSetCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetCompoundSystemDeflection._Cast_ConicalGearSetCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetCompoundSystemDeflection:
    """Special nested class for casting ConicalGearSetCompoundSystemDeflection to subclasses."""

    __parent__: "ConicalGearSetCompoundSystemDeflection"

    @property
    def gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3155.GearSetCompoundSystemDeflection":
        return self.__parent__._cast(_3155.GearSetCompoundSystemDeflection)

    @property
    def specialised_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3196.SpecialisedAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3196,
        )

        return self.__parent__._cast(_3196.SpecialisedAssemblyCompoundSystemDeflection)

    @property
    def abstract_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3094.AbstractAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3094,
        )

        return self.__parent__._cast(_3094.AbstractAssemblyCompoundSystemDeflection)

    @property
    def part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3176.PartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3176,
        )

        return self.__parent__._cast(_3176.PartCompoundSystemDeflection)

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
    def agma_gleason_conical_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3100.AGMAGleasonConicalGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3100,
        )

        return self.__parent__._cast(
            _3100.AGMAGleasonConicalGearSetCompoundSystemDeflection
        )

    @property
    def bevel_differential_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3107.BevelDifferentialGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3107,
        )

        return self.__parent__._cast(
            _3107.BevelDifferentialGearSetCompoundSystemDeflection
        )

    @property
    def bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3112.BevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3112,
        )

        return self.__parent__._cast(_3112.BevelGearSetCompoundSystemDeflection)

    @property
    def hypoid_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3159.HypoidGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3159,
        )

        return self.__parent__._cast(_3159.HypoidGearSetCompoundSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3163.KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3163,
        )

        return self.__parent__._cast(
            _3163.KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3166.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3166,
        )

        return self.__parent__._cast(
            _3166.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3169.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3169,
        )

        return self.__parent__._cast(
            _3169.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection
        )

    @property
    def spiral_bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3199.SpiralBevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3199,
        )

        return self.__parent__._cast(_3199.SpiralBevelGearSetCompoundSystemDeflection)

    @property
    def straight_bevel_diff_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3205.StraightBevelDiffGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3205,
        )

        return self.__parent__._cast(
            _3205.StraightBevelDiffGearSetCompoundSystemDeflection
        )

    @property
    def straight_bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3208.StraightBevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3208,
        )

        return self.__parent__._cast(_3208.StraightBevelGearSetCompoundSystemDeflection)

    @property
    def zerol_bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3226.ZerolBevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3226,
        )

        return self.__parent__._cast(_3226.ZerolBevelGearSetCompoundSystemDeflection)

    @property
    def conical_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "ConicalGearSetCompoundSystemDeflection":
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
class ConicalGearSetCompoundSystemDeflection(_3155.GearSetCompoundSystemDeflection):
    """ConicalGearSetCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def conical_gear_set_duty_cycle_rating(
        self: "Self",
    ) -> "_632.ConicalGearSetDutyCycleRating":
        """mastapy.gears.rating.conical.ConicalGearSetDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDutyCycleRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_2966.ConicalGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConicalGearSetSystemDeflection]

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
    ) -> "List[_2966.ConicalGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConicalGearSetSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetCompoundSystemDeflection
        """
        return _Cast_ConicalGearSetCompoundSystemDeflection(self)
