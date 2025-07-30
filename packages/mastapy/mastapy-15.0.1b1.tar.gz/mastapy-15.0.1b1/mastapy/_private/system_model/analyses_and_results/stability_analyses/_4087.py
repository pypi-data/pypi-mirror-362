"""InterMountableComponentConnectionStabilityAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.stability_analyses import _4055

_INTER_MOUNTABLE_COMPONENT_CONNECTION_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "InterMountableComponentConnectionStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4024,
        _4029,
        _4031,
        _4036,
        _4041,
        _4046,
        _4049,
        _4052,
        _4057,
        _4061,
        _4068,
        _4075,
        _4080,
        _4084,
        _4088,
        _4091,
        _4094,
        _4104,
        _4114,
        _4116,
        _4123,
        _4126,
        _4132,
        _4135,
        _4144,
        _4150,
        _4153,
    )
    from mastapy._private.system_model.connections_and_sockets import _2502

    Self = TypeVar("Self", bound="InterMountableComponentConnectionStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionStabilityAnalysis:
    """Special nested class for casting InterMountableComponentConnectionStabilityAnalysis to subclasses."""

    __parent__: "InterMountableComponentConnectionStabilityAnalysis"

    @property
    def connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4055.ConnectionStabilityAnalysis":
        return self.__parent__._cast(_4055.ConnectionStabilityAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7883.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7883,
        )

        return self.__parent__._cast(_7883.ConnectionStaticLoadAnalysisCase)

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
    def agma_gleason_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4024.AGMAGleasonConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4024,
        )

        return self.__parent__._cast(_4024.AGMAGleasonConicalGearMeshStabilityAnalysis)

    @property
    def belt_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4029.BeltConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4029,
        )

        return self.__parent__._cast(_4029.BeltConnectionStabilityAnalysis)

    @property
    def bevel_differential_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4031.BevelDifferentialGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4031,
        )

        return self.__parent__._cast(_4031.BevelDifferentialGearMeshStabilityAnalysis)

    @property
    def bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4036.BevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4036,
        )

        return self.__parent__._cast(_4036.BevelGearMeshStabilityAnalysis)

    @property
    def clutch_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4041.ClutchConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4041,
        )

        return self.__parent__._cast(_4041.ClutchConnectionStabilityAnalysis)

    @property
    def concept_coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4046.ConceptCouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4046,
        )

        return self.__parent__._cast(_4046.ConceptCouplingConnectionStabilityAnalysis)

    @property
    def concept_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4049.ConceptGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4049,
        )

        return self.__parent__._cast(_4049.ConceptGearMeshStabilityAnalysis)

    @property
    def conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4052.ConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4052,
        )

        return self.__parent__._cast(_4052.ConicalGearMeshStabilityAnalysis)

    @property
    def coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4057.CouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4057,
        )

        return self.__parent__._cast(_4057.CouplingConnectionStabilityAnalysis)

    @property
    def cvt_belt_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4061.CVTBeltConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4061,
        )

        return self.__parent__._cast(_4061.CVTBeltConnectionStabilityAnalysis)

    @property
    def cylindrical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4068.CylindricalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4068,
        )

        return self.__parent__._cast(_4068.CylindricalGearMeshStabilityAnalysis)

    @property
    def face_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4075.FaceGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4075,
        )

        return self.__parent__._cast(_4075.FaceGearMeshStabilityAnalysis)

    @property
    def gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4080.GearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4080,
        )

        return self.__parent__._cast(_4080.GearMeshStabilityAnalysis)

    @property
    def hypoid_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4084.HypoidGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4084,
        )

        return self.__parent__._cast(_4084.HypoidGearMeshStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4088.KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4088,
        )

        return self.__parent__._cast(
            _4088.KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4091.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4091,
        )

        return self.__parent__._cast(
            _4091.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4094.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4094,
        )

        return self.__parent__._cast(
            _4094.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4104.PartToPartShearCouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4104,
        )

        return self.__parent__._cast(
            _4104.PartToPartShearCouplingConnectionStabilityAnalysis
        )

    @property
    def ring_pins_to_disc_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4114.RingPinsToDiscConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4114,
        )

        return self.__parent__._cast(_4114.RingPinsToDiscConnectionStabilityAnalysis)

    @property
    def rolling_ring_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4116.RollingRingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4116,
        )

        return self.__parent__._cast(_4116.RollingRingConnectionStabilityAnalysis)

    @property
    def spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4123.SpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4123,
        )

        return self.__parent__._cast(_4123.SpiralBevelGearMeshStabilityAnalysis)

    @property
    def spring_damper_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4126.SpringDamperConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4126,
        )

        return self.__parent__._cast(_4126.SpringDamperConnectionStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4132.StraightBevelDiffGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4132,
        )

        return self.__parent__._cast(_4132.StraightBevelDiffGearMeshStabilityAnalysis)

    @property
    def straight_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4135.StraightBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4135,
        )

        return self.__parent__._cast(_4135.StraightBevelGearMeshStabilityAnalysis)

    @property
    def torque_converter_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4144.TorqueConverterConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4144,
        )

        return self.__parent__._cast(_4144.TorqueConverterConnectionStabilityAnalysis)

    @property
    def worm_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4150.WormGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4150,
        )

        return self.__parent__._cast(_4150.WormGearMeshStabilityAnalysis)

    @property
    def zerol_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4153.ZerolBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4153,
        )

        return self.__parent__._cast(_4153.ZerolBevelGearMeshStabilityAnalysis)

    @property
    def inter_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionStabilityAnalysis":
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
class InterMountableComponentConnectionStabilityAnalysis(
    _4055.ConnectionStabilityAnalysis
):
    """InterMountableComponentConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTER_MOUNTABLE_COMPONENT_CONNECTION_STABILITY_ANALYSIS

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
    ) -> "_Cast_InterMountableComponentConnectionStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionStabilityAnalysis
        """
        return _Cast_InterMountableComponentConnectionStabilityAnalysis(self)
