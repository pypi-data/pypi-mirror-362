"""SpiralBevelGearSetParametricStudyTool"""

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
    _4579,
)

_SPIRAL_BEVEL_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "SpiralBevelGearSetParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7887
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4561,
        _4567,
        _4595,
        _4628,
        _4661,
        _4680,
        _4681,
        _4682,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7826
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3051,
    )
    from mastapy._private.system_model.part_model.gears import _2782

    Self = TypeVar("Self", bound="SpiralBevelGearSetParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpiralBevelGearSetParametricStudyTool._Cast_SpiralBevelGearSetParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearSetParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearSetParametricStudyTool:
    """Special nested class for casting SpiralBevelGearSetParametricStudyTool to subclasses."""

    __parent__: "SpiralBevelGearSetParametricStudyTool"

    @property
    def bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4579.BevelGearSetParametricStudyTool":
        return self.__parent__._cast(_4579.BevelGearSetParametricStudyTool)

    @property
    def agma_gleason_conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4567.AGMAGleasonConicalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4567,
        )

        return self.__parent__._cast(_4567.AGMAGleasonConicalGearSetParametricStudyTool)

    @property
    def conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4595.ConicalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4595,
        )

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
    def spiral_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "SpiralBevelGearSetParametricStudyTool":
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
class SpiralBevelGearSetParametricStudyTool(_4579.BevelGearSetParametricStudyTool):
    """SpiralBevelGearSetParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_GEAR_SET_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2782.SpiralBevelGearSet":
        """mastapy.system_model.part_model.gears.SpiralBevelGearSet

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
    def assembly_load_case(self: "Self") -> "_7826.SpiralBevelGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase

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
    def assembly_system_deflection_results(
        self: "Self",
    ) -> "List[_3051.SpiralBevelGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.SpiralBevelGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblySystemDeflectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def bevel_gears_parametric_study_tool(
        self: "Self",
    ) -> "List[_4682.SpiralBevelGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearsParametricStudyTool")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def spiral_bevel_gears_parametric_study_tool(
        self: "Self",
    ) -> "List[_4682.SpiralBevelGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpiralBevelGearsParametricStudyTool"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def bevel_meshes_parametric_study_tool(
        self: "Self",
    ) -> "List[_4681.SpiralBevelGearMeshParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearMeshParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelMeshesParametricStudyTool")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def spiral_bevel_meshes_parametric_study_tool(
        self: "Self",
    ) -> "List[_4681.SpiralBevelGearMeshParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearMeshParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpiralBevelMeshesParametricStudyTool"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelGearSetParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearSetParametricStudyTool
        """
        return _Cast_SpiralBevelGearSetParametricStudyTool(self)
