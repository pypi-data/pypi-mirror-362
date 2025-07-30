"""AGMAGleasonConicalGearMeshCompoundParametricStudyTool"""

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
    _4744,
)

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "AGMAGleasonConicalGearMeshCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4565,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4723,
        _4728,
        _4746,
        _4770,
        _4774,
        _4776,
        _4813,
        _4819,
        _4822,
        _4840,
    )

    Self = TypeVar(
        "Self", bound="AGMAGleasonConicalGearMeshCompoundParametricStudyTool"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshCompoundParametricStudyTool._Cast_AGMAGleasonConicalGearMeshCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshCompoundParametricStudyTool:
    """Special nested class for casting AGMAGleasonConicalGearMeshCompoundParametricStudyTool to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshCompoundParametricStudyTool"

    @property
    def conical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4744.ConicalGearMeshCompoundParametricStudyTool":
        return self.__parent__._cast(_4744.ConicalGearMeshCompoundParametricStudyTool)

    @property
    def gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4770.GearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4770,
        )

        return self.__parent__._cast(_4770.GearMeshCompoundParametricStudyTool)

    @property
    def inter_mountable_component_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4776.InterMountableComponentConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4776,
        )

        return self.__parent__._cast(
            _4776.InterMountableComponentConnectionCompoundParametricStudyTool
        )

    @property
    def connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4746.ConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4746,
        )

        return self.__parent__._cast(_4746.ConnectionCompoundParametricStudyTool)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7881.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7881,
        )

        return self.__parent__._cast(_7881.ConnectionCompoundAnalysis)

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
    def bevel_differential_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4723.BevelDifferentialGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4723,
        )

        return self.__parent__._cast(
            _4723.BevelDifferentialGearMeshCompoundParametricStudyTool
        )

    @property
    def bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4728.BevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4728,
        )

        return self.__parent__._cast(_4728.BevelGearMeshCompoundParametricStudyTool)

    @property
    def hypoid_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4774.HypoidGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4774,
        )

        return self.__parent__._cast(_4774.HypoidGearMeshCompoundParametricStudyTool)

    @property
    def spiral_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4813.SpiralBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4813,
        )

        return self.__parent__._cast(
            _4813.SpiralBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4819.StraightBevelDiffGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4819,
        )

        return self.__parent__._cast(
            _4819.StraightBevelDiffGearMeshCompoundParametricStudyTool
        )

    @property
    def straight_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4822.StraightBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4822,
        )

        return self.__parent__._cast(
            _4822.StraightBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def zerol_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4840.ZerolBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4840,
        )

        return self.__parent__._cast(
            _4840.ZerolBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshCompoundParametricStudyTool":
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
class AGMAGleasonConicalGearMeshCompoundParametricStudyTool(
    _4744.ConicalGearMeshCompoundParametricStudyTool
):
    """AGMAGleasonConicalGearMeshCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_PARAMETRIC_STUDY_TOOL
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4565.AGMAGleasonConicalGearMeshParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearMeshParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4565.AGMAGleasonConicalGearMeshParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearMeshParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AGMAGleasonConicalGearMeshCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshCompoundParametricStudyTool
        """
        return _Cast_AGMAGleasonConicalGearMeshCompoundParametricStudyTool(self)
