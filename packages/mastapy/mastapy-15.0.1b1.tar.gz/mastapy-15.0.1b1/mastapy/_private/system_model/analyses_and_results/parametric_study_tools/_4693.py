"""StraightBevelPlanetGearParametricStudyTool"""

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
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4688,
)

_STRAIGHT_BEVEL_PLANET_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "StraightBevelPlanetGearParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7887
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4566,
        _4578,
        _4586,
        _4594,
        _4627,
        _4648,
        _4661,
    )
    from mastapy._private.system_model.part_model.gears import _2787

    Self = TypeVar("Self", bound="StraightBevelPlanetGearParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelPlanetGearParametricStudyTool._Cast_StraightBevelPlanetGearParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelPlanetGearParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelPlanetGearParametricStudyTool:
    """Special nested class for casting StraightBevelPlanetGearParametricStudyTool to subclasses."""

    __parent__: "StraightBevelPlanetGearParametricStudyTool"

    @property
    def straight_bevel_diff_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4688.StraightBevelDiffGearParametricStudyTool":
        return self.__parent__._cast(_4688.StraightBevelDiffGearParametricStudyTool)

    @property
    def bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4578.BevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4578,
        )

        return self.__parent__._cast(_4578.BevelGearParametricStudyTool)

    @property
    def agma_gleason_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4566.AGMAGleasonConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4566,
        )

        return self.__parent__._cast(_4566.AGMAGleasonConicalGearParametricStudyTool)

    @property
    def conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4594.ConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4594,
        )

        return self.__parent__._cast(_4594.ConicalGearParametricStudyTool)

    @property
    def gear_parametric_study_tool(self: "CastSelf") -> "_4627.GearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4627,
        )

        return self.__parent__._cast(_4627.GearParametricStudyTool)

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
    def straight_bevel_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "StraightBevelPlanetGearParametricStudyTool":
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
class StraightBevelPlanetGearParametricStudyTool(
    _4688.StraightBevelDiffGearParametricStudyTool
):
    """StraightBevelPlanetGearParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_PLANET_GEAR_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2787.StraightBevelPlanetGear":
        """mastapy.system_model.part_model.gears.StraightBevelPlanetGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelPlanetGearParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelPlanetGearParametricStudyTool
        """
        return _Cast_StraightBevelPlanetGearParametricStudyTool(self)
