"""KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5562,
)

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
        "KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5464,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5528,
        _5588,
        _5599,
        _5602,
        _5609,
        _5628,
    )

    Self = TypeVar(
        "Self",
        bound="KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed._Cast_KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed"

    @property
    def conical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5562.ConicalGearSetCompoundModalAnalysisAtASpeed":
        return self.__parent__._cast(_5562.ConicalGearSetCompoundModalAnalysisAtASpeed)

    @property
    def gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5588.GearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5588,
        )

        return self.__parent__._cast(_5588.GearSetCompoundModalAnalysisAtASpeed)

    @property
    def specialised_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5628.SpecialisedAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5628,
        )

        return self.__parent__._cast(
            _5628.SpecialisedAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def abstract_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5528.AbstractAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5528,
        )

        return self.__parent__._cast(
            _5528.AbstractAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5609.PartCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5609,
        )

        return self.__parent__._cast(_5609.PartCompoundModalAnalysisAtASpeed)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5599.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5599,
        )

        return self.__parent__._cast(
            _5599.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_5602.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5602,
        )

        return self.__parent__._cast(
            _5602.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed":
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
class KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed(
    _5562.ConicalGearSetCompoundModalAnalysisAtASpeed
):
    """KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
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
    ) -> "List[_5464.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed]

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
    ) -> "List[_5464.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed]

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
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed
        """
        return (
            _Cast_KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed(
                self
            )
        )
