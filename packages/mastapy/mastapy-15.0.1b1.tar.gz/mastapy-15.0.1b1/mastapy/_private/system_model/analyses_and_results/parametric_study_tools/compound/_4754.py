"""CycloidalAssemblyCompoundParametricStudyTool"""

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

_CYCLOIDAL_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "CycloidalAssemblyCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4604,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4711,
        _4792,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7726
    from mastapy._private.system_model.part_model.cycloidal import _2806

    Self = TypeVar("Self", bound="CycloidalAssemblyCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalAssemblyCompoundParametricStudyTool._Cast_CycloidalAssemblyCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalAssemblyCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalAssemblyCompoundParametricStudyTool:
    """Special nested class for casting CycloidalAssemblyCompoundParametricStudyTool to subclasses."""

    __parent__: "CycloidalAssemblyCompoundParametricStudyTool"

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
    def cycloidal_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "CycloidalAssemblyCompoundParametricStudyTool":
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
class CycloidalAssemblyCompoundParametricStudyTool(
    _4811.SpecialisedAssemblyCompoundParametricStudyTool
):
    """CycloidalAssemblyCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2806.CycloidalAssembly":
        """mastapy.system_model.part_model.cycloidal.CycloidalAssembly

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
    def assembly_design(self: "Self") -> "_2806.CycloidalAssembly":
        """mastapy.system_model.part_model.cycloidal.CycloidalAssembly

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
    ) -> "_7726.CycloidalAssemblyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CycloidalAssemblyLoadCase

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
    ) -> "List[_4604.CycloidalAssemblyParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.CycloidalAssemblyParametricStudyTool]

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
    ) -> "List[_4604.CycloidalAssemblyParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.CycloidalAssemblyParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_CycloidalAssemblyCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_CycloidalAssemblyCompoundParametricStudyTool
        """
        return _Cast_CycloidalAssemblyCompoundParametricStudyTool(self)
