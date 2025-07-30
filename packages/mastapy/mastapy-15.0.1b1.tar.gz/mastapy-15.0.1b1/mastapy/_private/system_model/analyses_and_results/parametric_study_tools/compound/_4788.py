"""MicrophoneArrayCompoundParametricStudyTool"""

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
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4811,
)

_MICROPHONE_ARRAY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "MicrophoneArrayCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4645,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4711,
        _4792,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7793
    from mastapy._private.system_model.part_model import _2692

    Self = TypeVar("Self", bound="MicrophoneArrayCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicrophoneArrayCompoundParametricStudyTool._Cast_MicrophoneArrayCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicrophoneArrayCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicrophoneArrayCompoundParametricStudyTool:
    """Special nested class for casting MicrophoneArrayCompoundParametricStudyTool to subclasses."""

    __parent__: "MicrophoneArrayCompoundParametricStudyTool"

    @property
    def specialised_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4811.SpecialisedAssemblyCompoundParametricStudyTool":
        return self.__parent__._cast(
            _4811.SpecialisedAssemblyCompoundParametricStudyTool
        )

    @property
    def abstract_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4711.AbstractAssemblyCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4711,
        )

        return self.__parent__._cast(_4711.AbstractAssemblyCompoundParametricStudyTool)

    @property
    def part_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4792.PartCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4792,
        )

        return self.__parent__._cast(_4792.PartCompoundParametricStudyTool)

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
    def microphone_array_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "MicrophoneArrayCompoundParametricStudyTool":
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
class MicrophoneArrayCompoundParametricStudyTool(
    _4811.SpecialisedAssemblyCompoundParametricStudyTool
):
    """MicrophoneArrayCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICROPHONE_ARRAY_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2692.MicrophoneArray":
        """mastapy.system_model.part_model.MicrophoneArray

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
    def assembly_design(self: "Self") -> "_2692.MicrophoneArray":
        """mastapy.system_model.part_model.MicrophoneArray

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
    def properties_changing_all_load_cases(
        self: "Self",
    ) -> "_7793.MicrophoneArrayLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.MicrophoneArrayLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PropertiesChangingAllLoadCases")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4645.MicrophoneArrayParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.MicrophoneArrayParametricStudyTool]

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
    ) -> "List[_4645.MicrophoneArrayParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.MicrophoneArrayParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_MicrophoneArrayCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_MicrophoneArrayCompoundParametricStudyTool
        """
        return _Cast_MicrophoneArrayCompoundParametricStudyTool(self)
