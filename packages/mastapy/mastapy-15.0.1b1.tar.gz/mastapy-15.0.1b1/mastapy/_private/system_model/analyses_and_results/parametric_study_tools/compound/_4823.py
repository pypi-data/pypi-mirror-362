"""StraightBevelGearSetCompoundParametricStudyTool"""

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
    _4729,
)

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "StraightBevelGearSetCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4692,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4711,
        _4717,
        _4745,
        _4771,
        _4792,
        _4811,
        _4821,
        _4822,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7835
    from mastapy._private.system_model.part_model.gears import _2786

    Self = TypeVar("Self", bound="StraightBevelGearSetCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelGearSetCompoundParametricStudyTool._Cast_StraightBevelGearSetCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearSetCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelGearSetCompoundParametricStudyTool:
    """Special nested class for casting StraightBevelGearSetCompoundParametricStudyTool to subclasses."""

    __parent__: "StraightBevelGearSetCompoundParametricStudyTool"

    @property
    def bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4729.BevelGearSetCompoundParametricStudyTool":
        return self.__parent__._cast(_4729.BevelGearSetCompoundParametricStudyTool)

    @property
    def agma_gleason_conical_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4717.AGMAGleasonConicalGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4717,
        )

        return self.__parent__._cast(
            _4717.AGMAGleasonConicalGearSetCompoundParametricStudyTool
        )

    @property
    def conical_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4745.ConicalGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4745,
        )

        return self.__parent__._cast(_4745.ConicalGearSetCompoundParametricStudyTool)

    @property
    def gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4771.GearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4771,
        )

        return self.__parent__._cast(_4771.GearSetCompoundParametricStudyTool)

    @property
    def specialised_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4811.SpecialisedAssemblyCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4811,
        )

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
    def straight_bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "StraightBevelGearSetCompoundParametricStudyTool":
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
class StraightBevelGearSetCompoundParametricStudyTool(
    _4729.BevelGearSetCompoundParametricStudyTool
):
    """StraightBevelGearSetCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2786.StraightBevelGearSet":
        """mastapy.system_model.part_model.gears.StraightBevelGearSet

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
    def properties_changing_all_load_cases(
        self: "Self",
    ) -> "_7835.StraightBevelGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase

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
    ) -> "List[_4692.StraightBevelGearSetParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearSetParametricStudyTool]

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
    def straight_bevel_gears_compound_parametric_study_tool(
        self: "Self",
    ) -> "List[_4821.StraightBevelGearCompoundParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearCompoundParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelGearsCompoundParametricStudyTool"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def straight_bevel_meshes_compound_parametric_study_tool(
        self: "Self",
    ) -> "List[_4822.StraightBevelGearMeshCompoundParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearMeshCompoundParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelMeshesCompoundParametricStudyTool"
        )

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
    ) -> "List[_4692.StraightBevelGearSetParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearSetParametricStudyTool]

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
    ) -> "_Cast_StraightBevelGearSetCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelGearSetCompoundParametricStudyTool
        """
        return _Cast_StraightBevelGearSetCompoundParametricStudyTool(self)
