"""StraightBevelGearSetSteadyStateSynchronousResponse"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3245,
)

_STRAIGHT_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "StraightBevelGearSetSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7835
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3228,
        _3233,
        _3261,
        _3288,
        _3310,
        _3329,
        _3342,
        _3344,
    )
    from mastapy._private.system_model.part_model.gears import _2786

    Self = TypeVar("Self", bound="StraightBevelGearSetSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelGearSetSteadyStateSynchronousResponse._Cast_StraightBevelGearSetSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearSetSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelGearSetSteadyStateSynchronousResponse:
    """Special nested class for casting StraightBevelGearSetSteadyStateSynchronousResponse to subclasses."""

    __parent__: "StraightBevelGearSetSteadyStateSynchronousResponse"

    @property
    def bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3245.BevelGearSetSteadyStateSynchronousResponse":
        return self.__parent__._cast(_3245.BevelGearSetSteadyStateSynchronousResponse)

    @property
    def agma_gleason_conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3233.AGMAGleasonConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3233,
        )

        return self.__parent__._cast(
            _3233.AGMAGleasonConicalGearSetSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3261.ConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3261,
        )

        return self.__parent__._cast(_3261.ConicalGearSetSteadyStateSynchronousResponse)

    @property
    def gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3288.GearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3288,
        )

        return self.__parent__._cast(_3288.GearSetSteadyStateSynchronousResponse)

    @property
    def specialised_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3329.SpecialisedAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3329,
        )

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
    def straight_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "StraightBevelGearSetSteadyStateSynchronousResponse":
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
class StraightBevelGearSetSteadyStateSynchronousResponse(
    _3245.BevelGearSetSteadyStateSynchronousResponse
):
    """StraightBevelGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2786.StraightBevelGearSet":
        """mastapy.system_model.part_model.gears.StraightBevelGearSet

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
    def assembly_load_case(self: "Self") -> "_7835.StraightBevelGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase

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
    def bevel_gears_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3344.StraightBevelGearSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.StraightBevelGearSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelGearsSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def straight_bevel_gears_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3344.StraightBevelGearSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.StraightBevelGearSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelGearsSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def bevel_meshes_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3342.StraightBevelGearMeshSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.StraightBevelGearMeshSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelMeshesSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def straight_bevel_meshes_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3342.StraightBevelGearMeshSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.StraightBevelGearMeshSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelMeshesSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_StraightBevelGearSetSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelGearSetSteadyStateSynchronousResponse
        """
        return _Cast_StraightBevelGearSetSteadyStateSynchronousResponse(self)
