"""RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
    _3633,
)

_ROOT_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound",
    "RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3590,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
        _3626,
        _3707,
    )

    Self = TypeVar(
        "Self", bound="RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft"

    @property
    def assembly_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3633.AssemblyCompoundSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(
            _3633.AssemblyCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_assembly_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3626.AbstractAssemblyCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3626,
        )

        return self.__parent__._cast(
            _3626.AbstractAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3707.PartCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3707,
        )

        return self.__parent__._cast(
            _3707.PartCompoundSteadyStateSynchronousResponseOnAShaft
        )

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
    def root_assembly_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft":
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
class RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft(
    _3633.AssemblyCompoundSteadyStateSynchronousResponseOnAShaft
):
    """RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ROOT_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3590.RootAssemblySteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.RootAssemblySteadyStateSynchronousResponseOnAShaft]

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
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_3590.RootAssemblySteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.RootAssemblySteadyStateSynchronousResponseOnAShaft]

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
    ) -> "_Cast_RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft(self)
