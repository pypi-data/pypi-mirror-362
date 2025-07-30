"""ConceptGearMeshParametricStudyTool"""

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
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4626,
)

_CONCEPT_GEAR_MESH_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ConceptGearMeshParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7880
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4596,
        _4633,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7711
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2961,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2526

    Self = TypeVar("Self", bound="ConceptGearMeshParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConceptGearMeshParametricStudyTool._Cast_ConceptGearMeshParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearMeshParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearMeshParametricStudyTool:
    """Special nested class for casting ConceptGearMeshParametricStudyTool to subclasses."""

    __parent__: "ConceptGearMeshParametricStudyTool"

    @property
    def gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4626.GearMeshParametricStudyTool":
        return self.__parent__._cast(_4626.GearMeshParametricStudyTool)

    @property
    def inter_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4633.InterMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4633,
        )

        return self.__parent__._cast(
            _4633.InterMountableComponentConnectionParametricStudyTool
        )

    @property
    def connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4596.ConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4596,
        )

        return self.__parent__._cast(_4596.ConnectionParametricStudyTool)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7880.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7880,
        )

        return self.__parent__._cast(_7880.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2890.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.ConnectionAnalysis)

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
    def concept_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "ConceptGearMeshParametricStudyTool":
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
class ConceptGearMeshParametricStudyTool(_4626.GearMeshParametricStudyTool):
    """ConceptGearMeshParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_MESH_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2526.ConceptGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_load_case(self: "Self") -> "_7711.ConceptGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_system_deflection_results(
        self: "Self",
    ) -> "List[_2961.ConceptGearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConceptGearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionSystemDeflectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptGearMeshParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearMeshParametricStudyTool
        """
        return _Cast_ConceptGearMeshParametricStudyTool(self)
