"""AGMAGleasonConicalGearSetParametricStudyTool"""

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
    _4595,
)

_AGMA_GLEASON_CONICAL_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "AGMAGleasonConicalGearSetParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7887
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4561,
        _4565,
        _4566,
        _4574,
        _4579,
        _4628,
        _4632,
        _4661,
        _4680,
        _4683,
        _4689,
        _4692,
        _4710,
    )
    from mastapy._private.system_model.part_model.gears import _2751

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearSetParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearSetParametricStudyTool._Cast_AGMAGleasonConicalGearSetParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearSetParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearSetParametricStudyTool:
    """Special nested class for casting AGMAGleasonConicalGearSetParametricStudyTool to subclasses."""

    __parent__: "AGMAGleasonConicalGearSetParametricStudyTool"

    @property
    def conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4595.ConicalGearSetParametricStudyTool":
        return self.__parent__._cast(_4595.ConicalGearSetParametricStudyTool)

    @property
    def gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4628.GearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4628,
        )

        return self.__parent__._cast(_4628.GearSetParametricStudyTool)

    @property
    def specialised_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4680.SpecialisedAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4680,
        )

        return self.__parent__._cast(_4680.SpecialisedAssemblyParametricStudyTool)

    @property
    def abstract_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4561.AbstractAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4561,
        )

        return self.__parent__._cast(_4561.AbstractAssemblyParametricStudyTool)

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
    def bevel_differential_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4574.BevelDifferentialGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4574,
        )

        return self.__parent__._cast(_4574.BevelDifferentialGearSetParametricStudyTool)

    @property
    def bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4579.BevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4579,
        )

        return self.__parent__._cast(_4579.BevelGearSetParametricStudyTool)

    @property
    def hypoid_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4632.HypoidGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4632,
        )

        return self.__parent__._cast(_4632.HypoidGearSetParametricStudyTool)

    @property
    def spiral_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4683.SpiralBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4683,
        )

        return self.__parent__._cast(_4683.SpiralBevelGearSetParametricStudyTool)

    @property
    def straight_bevel_diff_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4689.StraightBevelDiffGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4689,
        )

        return self.__parent__._cast(_4689.StraightBevelDiffGearSetParametricStudyTool)

    @property
    def straight_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4692.StraightBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4692,
        )

        return self.__parent__._cast(_4692.StraightBevelGearSetParametricStudyTool)

    @property
    def zerol_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4710.ZerolBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4710,
        )

        return self.__parent__._cast(_4710.ZerolBevelGearSetParametricStudyTool)

    @property
    def agma_gleason_conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearSetParametricStudyTool":
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
class AGMAGleasonConicalGearSetParametricStudyTool(
    _4595.ConicalGearSetParametricStudyTool
):
    """AGMAGleasonConicalGearSetParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_SET_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2751.AGMAGleasonConicalGearSet":
        """mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet

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
    def conical_gears_parametric_study_tool(
        self: "Self",
    ) -> "List[_4566.AGMAGleasonConicalGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearsParametricStudyTool")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def agma_gleason_conical_gears_parametric_study_tool(
        self: "Self",
    ) -> "List[_4566.AGMAGleasonConicalGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAGleasonConicalGearsParametricStudyTool"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def conical_meshes_parametric_study_tool(
        self: "Self",
    ) -> "List[_4565.AGMAGleasonConicalGearMeshParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearMeshParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshesParametricStudyTool")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def agma_gleason_conical_meshes_parametric_study_tool(
        self: "Self",
    ) -> "List[_4565.AGMAGleasonConicalGearMeshParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearMeshParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAGleasonConicalMeshesParametricStudyTool"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearSetParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearSetParametricStudyTool
        """
        return _Cast_AGMAGleasonConicalGearSetParametricStudyTool(self)
