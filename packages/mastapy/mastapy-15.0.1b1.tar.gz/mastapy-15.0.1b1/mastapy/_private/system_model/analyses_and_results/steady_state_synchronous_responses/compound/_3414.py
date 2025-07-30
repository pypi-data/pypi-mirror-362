"""DatumCompoundSteadyStateSynchronousResponse"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3388,
)

_DATUM_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "DatumCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3279,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3444,
    )
    from mastapy._private.system_model.part_model import _2674

    Self = TypeVar("Self", bound="DatumCompoundSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DatumCompoundSteadyStateSynchronousResponse._Cast_DatumCompoundSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DatumCompoundSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DatumCompoundSteadyStateSynchronousResponse:
    """Special nested class for casting DatumCompoundSteadyStateSynchronousResponse to subclasses."""

    __parent__: "DatumCompoundSteadyStateSynchronousResponse"

    @property
    def component_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3388.ComponentCompoundSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3388.ComponentCompoundSteadyStateSynchronousResponse
        )

    @property
    def part_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3444.PartCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3444,
        )

        return self.__parent__._cast(_3444.PartCompoundSteadyStateSynchronousResponse)

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
    def datum_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "DatumCompoundSteadyStateSynchronousResponse":
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
class DatumCompoundSteadyStateSynchronousResponse(
    _3388.ComponentCompoundSteadyStateSynchronousResponse
):
    """DatumCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATUM_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2674.Datum":
        """mastapy.system_model.part_model.Datum

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
    ) -> "List[_3279.DatumSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.DatumSteadyStateSynchronousResponse]

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
    ) -> "List[_3279.DatumSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.DatumSteadyStateSynchronousResponse]

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
    def cast_to(self: "Self") -> "_Cast_DatumCompoundSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_DatumCompoundSteadyStateSynchronousResponse
        """
        return _Cast_DatumCompoundSteadyStateSynchronousResponse(self)
