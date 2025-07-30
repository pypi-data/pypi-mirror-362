"""ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
    _3651,
)

_EXTERNAL_CAD_MODEL_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound",
    "ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3546,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
        _3707,
    )
    from mastapy._private.system_model.part_model import _2679

    Self = TypeVar(
        "Self", bound="ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft._Cast_ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft"

    @property
    def component_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3651.ComponentCompoundSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(
            _3651.ComponentCompoundSteadyStateSynchronousResponseOnAShaft
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
    def external_cad_model_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft":
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
class ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft(
    _3651.ComponentCompoundSteadyStateSynchronousResponseOnAShaft
):
    """ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _EXTERNAL_CAD_MODEL_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3546.ExternalCADModelSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.ExternalCADModelSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_3546.ExternalCADModelSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.ExternalCADModelSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft(
            self
        )
