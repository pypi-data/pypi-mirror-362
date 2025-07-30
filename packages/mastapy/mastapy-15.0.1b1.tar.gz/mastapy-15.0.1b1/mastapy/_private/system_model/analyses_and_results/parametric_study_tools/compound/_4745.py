"""ConicalGearSetCompoundParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4771,
)

_CONICAL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "ConicalGearSetCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4595,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4711,
        _4717,
        _4724,
        _4729,
        _4775,
        _4779,
        _4782,
        _4785,
        _4792,
        _4811,
        _4814,
        _4820,
        _4823,
        _4841,
    )

    Self = TypeVar("Self", bound="ConicalGearSetCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetCompoundParametricStudyTool._Cast_ConicalGearSetCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetCompoundParametricStudyTool:
    """Special nested class for casting ConicalGearSetCompoundParametricStudyTool to subclasses."""

    __parent__: "ConicalGearSetCompoundParametricStudyTool"

    @property
    def gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4771.GearSetCompoundParametricStudyTool":
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
    def bevel_differential_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4724.BevelDifferentialGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4724,
        )

        return self.__parent__._cast(
            _4724.BevelDifferentialGearSetCompoundParametricStudyTool
        )

    @property
    def bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4729.BevelGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4729,
        )

        return self.__parent__._cast(_4729.BevelGearSetCompoundParametricStudyTool)

    @property
    def hypoid_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4775.HypoidGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4775,
        )

        return self.__parent__._cast(_4775.HypoidGearSetCompoundParametricStudyTool)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4779.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4779,
        )

        return self.__parent__._cast(
            _4779.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4782.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4782,
        )

        return self.__parent__._cast(
            _4782.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4785.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4785,
        )

        return self.__parent__._cast(
            _4785.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool
        )

    @property
    def spiral_bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4814.SpiralBevelGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4814,
        )

        return self.__parent__._cast(
            _4814.SpiralBevelGearSetCompoundParametricStudyTool
        )

    @property
    def straight_bevel_diff_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4820.StraightBevelDiffGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4820,
        )

        return self.__parent__._cast(
            _4820.StraightBevelDiffGearSetCompoundParametricStudyTool
        )

    @property
    def straight_bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4823.StraightBevelGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4823,
        )

        return self.__parent__._cast(
            _4823.StraightBevelGearSetCompoundParametricStudyTool
        )

    @property
    def zerol_bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4841.ZerolBevelGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4841,
        )

        return self.__parent__._cast(_4841.ZerolBevelGearSetCompoundParametricStudyTool)

    @property
    def conical_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "ConicalGearSetCompoundParametricStudyTool":
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
class ConicalGearSetCompoundParametricStudyTool(
    _4771.GearSetCompoundParametricStudyTool
):
    """ConicalGearSetCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_4595.ConicalGearSetParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearSetParametricStudyTool]

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
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4595.ConicalGearSetParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearSetParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetCompoundParametricStudyTool
        """
        return _Cast_ConicalGearSetCompoundParametricStudyTool(self)
