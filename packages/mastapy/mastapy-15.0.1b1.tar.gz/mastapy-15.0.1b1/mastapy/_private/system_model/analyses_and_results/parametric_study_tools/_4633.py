"""InterMountableComponentConnectionParametricStudyTool"""

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
    _4596,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "InterMountableComponentConnectionParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7880
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4565,
        _4570,
        _4572,
        _4577,
        _4582,
        _4587,
        _4590,
        _4593,
        _4598,
        _4601,
        _4608,
        _4621,
        _4626,
        _4630,
        _4634,
        _4637,
        _4640,
        _4662,
        _4672,
        _4674,
        _4681,
        _4684,
        _4687,
        _4690,
        _4699,
        _4705,
        _4708,
    )
    from mastapy._private.system_model.connections_and_sockets import _2502

    Self = TypeVar("Self", bound="InterMountableComponentConnectionParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionParametricStudyTool._Cast_InterMountableComponentConnectionParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionParametricStudyTool:
    """Special nested class for casting InterMountableComponentConnectionParametricStudyTool to subclasses."""

    __parent__: "InterMountableComponentConnectionParametricStudyTool"

    @property
    def connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4596.ConnectionParametricStudyTool":
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
    def agma_gleason_conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4565.AGMAGleasonConicalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4565,
        )

        return self.__parent__._cast(
            _4565.AGMAGleasonConicalGearMeshParametricStudyTool
        )

    @property
    def belt_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4570.BeltConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4570,
        )

        return self.__parent__._cast(_4570.BeltConnectionParametricStudyTool)

    @property
    def bevel_differential_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4572.BevelDifferentialGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4572,
        )

        return self.__parent__._cast(_4572.BevelDifferentialGearMeshParametricStudyTool)

    @property
    def bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4577.BevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4577,
        )

        return self.__parent__._cast(_4577.BevelGearMeshParametricStudyTool)

    @property
    def clutch_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4582.ClutchConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4582,
        )

        return self.__parent__._cast(_4582.ClutchConnectionParametricStudyTool)

    @property
    def concept_coupling_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4587.ConceptCouplingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4587,
        )

        return self.__parent__._cast(_4587.ConceptCouplingConnectionParametricStudyTool)

    @property
    def concept_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4590.ConceptGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4590,
        )

        return self.__parent__._cast(_4590.ConceptGearMeshParametricStudyTool)

    @property
    def conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4593.ConicalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4593,
        )

        return self.__parent__._cast(_4593.ConicalGearMeshParametricStudyTool)

    @property
    def coupling_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4598.CouplingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4598,
        )

        return self.__parent__._cast(_4598.CouplingConnectionParametricStudyTool)

    @property
    def cvt_belt_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4601.CVTBeltConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4601,
        )

        return self.__parent__._cast(_4601.CVTBeltConnectionParametricStudyTool)

    @property
    def cylindrical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4608.CylindricalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4608,
        )

        return self.__parent__._cast(_4608.CylindricalGearMeshParametricStudyTool)

    @property
    def face_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4621.FaceGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4621,
        )

        return self.__parent__._cast(_4621.FaceGearMeshParametricStudyTool)

    @property
    def gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4626.GearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4626,
        )

        return self.__parent__._cast(_4626.GearMeshParametricStudyTool)

    @property
    def hypoid_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4630.HypoidGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4630,
        )

        return self.__parent__._cast(_4630.HypoidGearMeshParametricStudyTool)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4634.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4634,
        )

        return self.__parent__._cast(
            _4634.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool
        )

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
    def part_to_part_shear_coupling_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4662.PartToPartShearCouplingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4662,
        )

        return self.__parent__._cast(
            _4662.PartToPartShearCouplingConnectionParametricStudyTool
        )

    @property
    def ring_pins_to_disc_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4672.RingPinsToDiscConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4672,
        )

        return self.__parent__._cast(_4672.RingPinsToDiscConnectionParametricStudyTool)

    @property
    def rolling_ring_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4674.RollingRingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4674,
        )

        return self.__parent__._cast(_4674.RollingRingConnectionParametricStudyTool)

    @property
    def spiral_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4681.SpiralBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4681,
        )

        return self.__parent__._cast(_4681.SpiralBevelGearMeshParametricStudyTool)

    @property
    def spring_damper_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4684.SpringDamperConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4684,
        )

        return self.__parent__._cast(_4684.SpringDamperConnectionParametricStudyTool)

    @property
    def straight_bevel_diff_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4687.StraightBevelDiffGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4687,
        )

        return self.__parent__._cast(_4687.StraightBevelDiffGearMeshParametricStudyTool)

    @property
    def straight_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4690.StraightBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4690,
        )

        return self.__parent__._cast(_4690.StraightBevelGearMeshParametricStudyTool)

    @property
    def torque_converter_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4699.TorqueConverterConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4699,
        )

        return self.__parent__._cast(_4699.TorqueConverterConnectionParametricStudyTool)

    @property
    def worm_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4705.WormGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4705,
        )

        return self.__parent__._cast(_4705.WormGearMeshParametricStudyTool)

    @property
    def zerol_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4708.ZerolBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4708,
        )

        return self.__parent__._cast(_4708.ZerolBevelGearMeshParametricStudyTool)

    @property
    def inter_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionParametricStudyTool":
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
class InterMountableComponentConnectionParametricStudyTool(
    _4596.ConnectionParametricStudyTool
):
    """InterMountableComponentConnectionParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTER_MOUNTABLE_COMPONENT_CONNECTION_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2502.InterMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.InterMountableComponentConnection

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
    ) -> "_Cast_InterMountableComponentConnectionParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionParametricStudyTool
        """
        return _Cast_InterMountableComponentConnectionParametricStudyTool(self)
