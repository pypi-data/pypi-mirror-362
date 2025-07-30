"""InterMountableComponentConnectionHarmonicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6005

_INTER_MOUNTABLE_COMPONENT_CONNECTION_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "InterMountableComponentConnectionHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5974,
        _5978,
        _5981,
        _5986,
        _5990,
        _5996,
        _6000,
        _6003,
        _6007,
        _6010,
        _6018,
        _6039,
        _6046,
        _6065,
        _6069,
        _6072,
        _6075,
        _6085,
        _6097,
        _6099,
        _6109,
        _6111,
        _6116,
        _6119,
        _6127,
        _6135,
        _6138,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3008,
    )
    from mastapy._private.system_model.connections_and_sockets import _2502

    Self = TypeVar("Self", bound="InterMountableComponentConnectionHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionHarmonicAnalysis._Cast_InterMountableComponentConnectionHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionHarmonicAnalysis:
    """Special nested class for casting InterMountableComponentConnectionHarmonicAnalysis to subclasses."""

    __parent__: "InterMountableComponentConnectionHarmonicAnalysis"

    @property
    def connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6005.ConnectionHarmonicAnalysis":
        return self.__parent__._cast(_6005.ConnectionHarmonicAnalysis)

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
    def agma_gleason_conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5974.AGMAGleasonConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5974,
        )

        return self.__parent__._cast(_5974.AGMAGleasonConicalGearMeshHarmonicAnalysis)

    @property
    def belt_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5978.BeltConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5978,
        )

        return self.__parent__._cast(_5978.BeltConnectionHarmonicAnalysis)

    @property
    def bevel_differential_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5981.BevelDifferentialGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5981,
        )

        return self.__parent__._cast(_5981.BevelDifferentialGearMeshHarmonicAnalysis)

    @property
    def bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5986.BevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5986,
        )

        return self.__parent__._cast(_5986.BevelGearMeshHarmonicAnalysis)

    @property
    def clutch_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5990.ClutchConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5990,
        )

        return self.__parent__._cast(_5990.ClutchConnectionHarmonicAnalysis)

    @property
    def concept_coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5996.ConceptCouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5996,
        )

        return self.__parent__._cast(_5996.ConceptCouplingConnectionHarmonicAnalysis)

    @property
    def concept_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6000.ConceptGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6000,
        )

        return self.__parent__._cast(_6000.ConceptGearMeshHarmonicAnalysis)

    @property
    def conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6003.ConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6003,
        )

        return self.__parent__._cast(_6003.ConicalGearMeshHarmonicAnalysis)

    @property
    def coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6007.CouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6007,
        )

        return self.__parent__._cast(_6007.CouplingConnectionHarmonicAnalysis)

    @property
    def cvt_belt_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6010.CVTBeltConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6010,
        )

        return self.__parent__._cast(_6010.CVTBeltConnectionHarmonicAnalysis)

    @property
    def cylindrical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6018.CylindricalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6018,
        )

        return self.__parent__._cast(_6018.CylindricalGearMeshHarmonicAnalysis)

    @property
    def face_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6039.FaceGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6039,
        )

        return self.__parent__._cast(_6039.FaceGearMeshHarmonicAnalysis)

    @property
    def gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6046.GearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6046,
        )

        return self.__parent__._cast(_6046.GearMeshHarmonicAnalysis)

    @property
    def hypoid_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6065.HypoidGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6065,
        )

        return self.__parent__._cast(_6065.HypoidGearMeshHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6069.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6069,
        )

        return self.__parent__._cast(
            _6069.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6072.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6072,
        )

        return self.__parent__._cast(
            _6072.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6075.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6075,
        )

        return self.__parent__._cast(
            _6075.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6085.PartToPartShearCouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6085,
        )

        return self.__parent__._cast(
            _6085.PartToPartShearCouplingConnectionHarmonicAnalysis
        )

    @property
    def ring_pins_to_disc_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6097.RingPinsToDiscConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6097,
        )

        return self.__parent__._cast(_6097.RingPinsToDiscConnectionHarmonicAnalysis)

    @property
    def rolling_ring_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6099.RollingRingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6099,
        )

        return self.__parent__._cast(_6099.RollingRingConnectionHarmonicAnalysis)

    @property
    def spiral_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6109.SpiralBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6109,
        )

        return self.__parent__._cast(_6109.SpiralBevelGearMeshHarmonicAnalysis)

    @property
    def spring_damper_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6111.SpringDamperConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6111,
        )

        return self.__parent__._cast(_6111.SpringDamperConnectionHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6116.StraightBevelDiffGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6116,
        )

        return self.__parent__._cast(_6116.StraightBevelDiffGearMeshHarmonicAnalysis)

    @property
    def straight_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6119.StraightBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6119,
        )

        return self.__parent__._cast(_6119.StraightBevelGearMeshHarmonicAnalysis)

    @property
    def torque_converter_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6127.TorqueConverterConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6127,
        )

        return self.__parent__._cast(_6127.TorqueConverterConnectionHarmonicAnalysis)

    @property
    def worm_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6135.WormGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6135,
        )

        return self.__parent__._cast(_6135.WormGearMeshHarmonicAnalysis)

    @property
    def zerol_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6138.ZerolBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6138,
        )

        return self.__parent__._cast(_6138.ZerolBevelGearMeshHarmonicAnalysis)

    @property
    def inter_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionHarmonicAnalysis":
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
class InterMountableComponentConnectionHarmonicAnalysis(
    _6005.ConnectionHarmonicAnalysis
):
    """InterMountableComponentConnectionHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTER_MOUNTABLE_COMPONENT_CONNECTION_HARMONIC_ANALYSIS

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
    @exception_bridge
    def system_deflection_results(
        self: "Self",
    ) -> "_3008.InterMountableComponentConnectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.InterMountableComponentConnectionSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_InterMountableComponentConnectionHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionHarmonicAnalysis
        """
        return _Cast_InterMountableComponentConnectionHarmonicAnalysis(self)
