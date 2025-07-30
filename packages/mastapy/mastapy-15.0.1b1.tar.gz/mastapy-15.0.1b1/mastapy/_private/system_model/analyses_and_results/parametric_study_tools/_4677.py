"""ShaftHubConnectionParametricStudyTool"""

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
    _4597,
)

_SHAFT_HUB_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ShaftHubConnectionParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7887
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4586,
        _4648,
        _4661,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7820
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3044,
    )
    from mastapy._private.system_model.part_model.couplings import _2840

    Self = TypeVar("Self", bound="ShaftHubConnectionParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftHubConnectionParametricStudyTool._Cast_ShaftHubConnectionParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftHubConnectionParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftHubConnectionParametricStudyTool:
    """Special nested class for casting ShaftHubConnectionParametricStudyTool to subclasses."""

    __parent__: "ShaftHubConnectionParametricStudyTool"

    @property
    def connector_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4597.ConnectorParametricStudyTool":
        return self.__parent__._cast(_4597.ConnectorParametricStudyTool)

    @property
    def mountable_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4648.MountableComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4648,
        )

        return self.__parent__._cast(_4648.MountableComponentParametricStudyTool)

    @property
    def component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4586.ComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4586,
        )

        return self.__parent__._cast(_4586.ComponentParametricStudyTool)

    @property
    def part_parametric_study_tool(self: "CastSelf") -> "_4661.PartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4661,
        )

        return self.__parent__._cast(_4661.PartParametricStudyTool)

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
    def shaft_hub_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "ShaftHubConnectionParametricStudyTool":
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
class ShaftHubConnectionParametricStudyTool(_4597.ConnectorParametricStudyTool):
    """ShaftHubConnectionParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_HUB_CONNECTION_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2840.ShaftHubConnection":
        """mastapy.system_model.part_model.couplings.ShaftHubConnection

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
    def component_load_case(self: "Self") -> "_7820.ShaftHubConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def component_system_deflection_results(
        self: "Self",
    ) -> "List[_3044.ShaftHubConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ShaftHubConnectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentSystemDeflectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def planetaries(self: "Self") -> "List[ShaftHubConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftHubConnectionParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftHubConnectionParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ShaftHubConnectionParametricStudyTool
        """
        return _Cast_ShaftHubConnectionParametricStudyTool(self)
