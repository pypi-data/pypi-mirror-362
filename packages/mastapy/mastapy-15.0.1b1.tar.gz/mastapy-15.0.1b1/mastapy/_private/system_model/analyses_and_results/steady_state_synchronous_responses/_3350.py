"""SynchroniserSteadyStateSynchronousResponse"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3329,
)

_SYNCHRONISER_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "SynchroniserSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7839
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3228,
        _3310,
    )
    from mastapy._private.system_model.part_model.couplings import _2848

    Self = TypeVar("Self", bound="SynchroniserSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SynchroniserSteadyStateSynchronousResponse._Cast_SynchroniserSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SynchroniserSteadyStateSynchronousResponse:
    """Special nested class for casting SynchroniserSteadyStateSynchronousResponse to subclasses."""

    __parent__: "SynchroniserSteadyStateSynchronousResponse"

    @property
    def specialised_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3329.SpecialisedAssemblySteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3329.SpecialisedAssemblySteadyStateSynchronousResponse
        )

    @property
    def abstract_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3228.AbstractAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3228,
        )

        return self.__parent__._cast(
            _3228.AbstractAssemblySteadyStateSynchronousResponse
        )

    @property
    def part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3310.PartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3310,
        )

        return self.__parent__._cast(_3310.PartSteadyStateSynchronousResponse)

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
    def synchroniser_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "SynchroniserSteadyStateSynchronousResponse":
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
class SynchroniserSteadyStateSynchronousResponse(
    _3329.SpecialisedAssemblySteadyStateSynchronousResponse
):
    """SynchroniserSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYNCHRONISER_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2848.Synchroniser":
        """mastapy.system_model.part_model.couplings.Synchroniser

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
    def assembly_load_case(self: "Self") -> "_7839.SynchroniserLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SynchroniserSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_SynchroniserSteadyStateSynchronousResponse
        """
        return _Cast_SynchroniserSteadyStateSynchronousResponse(self)
