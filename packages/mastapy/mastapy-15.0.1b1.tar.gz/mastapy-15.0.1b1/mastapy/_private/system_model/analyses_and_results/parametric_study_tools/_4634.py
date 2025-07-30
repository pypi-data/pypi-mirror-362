"""KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool"""

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
    _4593,
)

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7880
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4596,
        _4626,
        _4633,
        _4637,
        _4640,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2539

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool._Cast_KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool"

    @property
    def conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4593.ConicalGearMeshParametricStudyTool":
        return self.__parent__._cast(_4593.ConicalGearMeshParametricStudyTool)

    @property
    def gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4626.GearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4626,
        )

        return self.__parent__._cast(_4626.GearMeshParametricStudyTool)

    @property
    def inter_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4633.InterMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4633,
        )

        return self.__parent__._cast(
            _4633.InterMountableComponentConnectionParametricStudyTool
        )

    @property
    def connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4596.ConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4596,
        )

        return self.__parent__._cast(_4596.ConnectionParametricStudyTool)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7880.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7880,
        )

        return self.__parent__._cast(_7880.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2890.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.ConnectionAnalysis)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4637.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4637,
        )

        return self.__parent__._cast(
            _4637.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4640.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4640,
        )

        return self.__parent__._cast(
            _4640.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool":
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
class KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool(
    _4593.ConicalGearMeshParametricStudyTool
):
    """KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_PARAMETRIC_STUDY_TOOL
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(
        self: "Self",
    ) -> "_2539.KlingelnbergCycloPalloidConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool(self)
