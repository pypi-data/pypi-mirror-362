"""CylindricalGearSetSteadyStateSynchronousResponse"""

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
    _3288,
)

_CYLINDRICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "CylindricalGearSetSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7734
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3228,
        _3275,
        _3277,
        _3310,
        _3315,
        _3329,
    )
    from mastapy._private.system_model.part_model.gears import _2763

    Self = TypeVar("Self", bound="CylindricalGearSetSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetSteadyStateSynchronousResponse._Cast_CylindricalGearSetSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetSteadyStateSynchronousResponse:
    """Special nested class for casting CylindricalGearSetSteadyStateSynchronousResponse to subclasses."""

    __parent__: "CylindricalGearSetSteadyStateSynchronousResponse"

    @property
    def gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3288.GearSetSteadyStateSynchronousResponse":
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
    def planetary_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3315.PlanetaryGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3315,
        )

        return self.__parent__._cast(
            _3315.PlanetaryGearSetSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "CylindricalGearSetSteadyStateSynchronousResponse":
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
class CylindricalGearSetSteadyStateSynchronousResponse(
    _3288.GearSetSteadyStateSynchronousResponse
):
    """CylindricalGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2763.CylindricalGearSet":
        """mastapy.system_model.part_model.gears.CylindricalGearSet

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
    def assembly_load_case(self: "Self") -> "_7734.CylindricalGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase

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
    def gears_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3277.CylindricalGearSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.CylindricalGearSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearsSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_gears_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3277.CylindricalGearSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.CylindricalGearSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearsSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3275.CylindricalGearMeshSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.CylindricalGearMeshSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshesSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_meshes_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3275.CylindricalGearMeshSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.CylindricalGearMeshSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalMeshesSteadyStateSynchronousResponse"
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
    ) -> "_Cast_CylindricalGearSetSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetSteadyStateSynchronousResponse
        """
        return _Cast_CylindricalGearSetSteadyStateSynchronousResponse(self)
