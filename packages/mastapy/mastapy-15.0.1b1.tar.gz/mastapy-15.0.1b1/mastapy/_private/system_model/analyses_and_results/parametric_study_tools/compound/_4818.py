"""StraightBevelDiffGearCompoundParametricStudyTool"""

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
    _4727,
)

_STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "StraightBevelDiffGearCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4688,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4715,
        _4736,
        _4743,
        _4769,
        _4790,
        _4792,
        _4824,
        _4825,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7830
    from mastapy._private.system_model.part_model.gears import _2783

    Self = TypeVar("Self", bound="StraightBevelDiffGearCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearCompoundParametricStudyTool._Cast_StraightBevelDiffGearCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearCompoundParametricStudyTool:
    """Special nested class for casting StraightBevelDiffGearCompoundParametricStudyTool to subclasses."""

    __parent__: "StraightBevelDiffGearCompoundParametricStudyTool"

    @property
    def bevel_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4727.BevelGearCompoundParametricStudyTool":
        return self.__parent__._cast(_4727.BevelGearCompoundParametricStudyTool)

    @property
    def agma_gleason_conical_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4715.AGMAGleasonConicalGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4715,
        )

        return self.__parent__._cast(
            _4715.AGMAGleasonConicalGearCompoundParametricStudyTool
        )

    @property
    def conical_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4743.ConicalGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4743,
        )

        return self.__parent__._cast(_4743.ConicalGearCompoundParametricStudyTool)

    @property
    def gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4769.GearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4769,
        )

        return self.__parent__._cast(_4769.GearCompoundParametricStudyTool)

    @property
    def mountable_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4790.MountableComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4790,
        )

        return self.__parent__._cast(
            _4790.MountableComponentCompoundParametricStudyTool
        )

    @property
    def component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4736.ComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4736,
        )

        return self.__parent__._cast(_4736.ComponentCompoundParametricStudyTool)

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
    def straight_bevel_planet_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4824.StraightBevelPlanetGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4824,
        )

        return self.__parent__._cast(
            _4824.StraightBevelPlanetGearCompoundParametricStudyTool
        )

    @property
    def straight_bevel_sun_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4825.StraightBevelSunGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4825,
        )

        return self.__parent__._cast(
            _4825.StraightBevelSunGearCompoundParametricStudyTool
        )

    @property
    def straight_bevel_diff_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearCompoundParametricStudyTool":
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
class StraightBevelDiffGearCompoundParametricStudyTool(
    _4727.BevelGearCompoundParametricStudyTool
):
    """StraightBevelDiffGearCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2783.StraightBevelDiffGear":
        """mastapy.system_model.part_model.gears.StraightBevelDiffGear

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
    def properties_changing_all_load_cases(
        self: "Self",
    ) -> "_7830.StraightBevelDiffGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase

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
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4688.StraightBevelDiffGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearParametricStudyTool]

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
    ) -> "List[_4688.StraightBevelDiffGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearParametricStudyTool]

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
    ) -> "_Cast_StraightBevelDiffGearCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearCompoundParametricStudyTool
        """
        return _Cast_StraightBevelDiffGearCompoundParametricStudyTool(self)
