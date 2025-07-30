"""ConnectionDynamicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7882

_CONNECTION_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "ConnectionDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6592,
        _6594,
        _6598,
        _6601,
        _6606,
        _6610,
        _6613,
        _6615,
        _6619,
        _6622,
        _6626,
        _6629,
        _6633,
        _6635,
        _6637,
        _6641,
        _6645,
        _6650,
        _6654,
        _6656,
        _6658,
        _6661,
        _6664,
        _6673,
        _6676,
        _6683,
        _6685,
        _6690,
        _6693,
        _6695,
        _6699,
        _6702,
        _6710,
        _6717,
        _6720,
    )
    from mastapy._private.system_model.connections_and_sockets import _2493

    Self = TypeVar("Self", bound="ConnectionDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="ConnectionDynamicAnalysis._Cast_ConnectionDynamicAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionDynamicAnalysis:
    """Special nested class for casting ConnectionDynamicAnalysis to subclasses."""

    __parent__: "ConnectionDynamicAnalysis"

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7882.ConnectionFEAnalysis":
        return self.__parent__._cast(_7882.ConnectionFEAnalysis)

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
    def abstract_shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6592.AbstractShaftToMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6592,
        )

        return self.__parent__._cast(
            _6592.AbstractShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6594.AGMAGleasonConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6594,
        )

        return self.__parent__._cast(_6594.AGMAGleasonConicalGearMeshDynamicAnalysis)

    @property
    def belt_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6598.BeltConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6598,
        )

        return self.__parent__._cast(_6598.BeltConnectionDynamicAnalysis)

    @property
    def bevel_differential_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6601.BevelDifferentialGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6601,
        )

        return self.__parent__._cast(_6601.BevelDifferentialGearMeshDynamicAnalysis)

    @property
    def bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6606.BevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6606,
        )

        return self.__parent__._cast(_6606.BevelGearMeshDynamicAnalysis)

    @property
    def clutch_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6610.ClutchConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6610,
        )

        return self.__parent__._cast(_6610.ClutchConnectionDynamicAnalysis)

    @property
    def coaxial_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6613.CoaxialConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6613,
        )

        return self.__parent__._cast(_6613.CoaxialConnectionDynamicAnalysis)

    @property
    def concept_coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6615.ConceptCouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6615,
        )

        return self.__parent__._cast(_6615.ConceptCouplingConnectionDynamicAnalysis)

    @property
    def concept_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6619.ConceptGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6619,
        )

        return self.__parent__._cast(_6619.ConceptGearMeshDynamicAnalysis)

    @property
    def conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6622.ConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6622,
        )

        return self.__parent__._cast(_6622.ConicalGearMeshDynamicAnalysis)

    @property
    def coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6626.CouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6626,
        )

        return self.__parent__._cast(_6626.CouplingConnectionDynamicAnalysis)

    @property
    def cvt_belt_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6629.CVTBeltConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6629,
        )

        return self.__parent__._cast(_6629.CVTBeltConnectionDynamicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6633.CycloidalDiscCentralBearingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6633,
        )

        return self.__parent__._cast(
            _6633.CycloidalDiscCentralBearingConnectionDynamicAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6635.CycloidalDiscPlanetaryBearingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6635,
        )

        return self.__parent__._cast(
            _6635.CycloidalDiscPlanetaryBearingConnectionDynamicAnalysis
        )

    @property
    def cylindrical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6637.CylindricalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6637,
        )

        return self.__parent__._cast(_6637.CylindricalGearMeshDynamicAnalysis)

    @property
    def face_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6645.FaceGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6645,
        )

        return self.__parent__._cast(_6645.FaceGearMeshDynamicAnalysis)

    @property
    def gear_mesh_dynamic_analysis(self: "CastSelf") -> "_6650.GearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6650,
        )

        return self.__parent__._cast(_6650.GearMeshDynamicAnalysis)

    @property
    def hypoid_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6654.HypoidGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6654,
        )

        return self.__parent__._cast(_6654.HypoidGearMeshDynamicAnalysis)

    @property
    def inter_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6656.InterMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6656,
        )

        return self.__parent__._cast(
            _6656.InterMountableComponentConnectionDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6658.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6658,
        )

        return self.__parent__._cast(
            _6658.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6661.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6661,
        )

        return self.__parent__._cast(
            _6661.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6664.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6664,
        )

        return self.__parent__._cast(
            _6664.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6673.PartToPartShearCouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6673,
        )

        return self.__parent__._cast(
            _6673.PartToPartShearCouplingConnectionDynamicAnalysis
        )

    @property
    def planetary_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6676.PlanetaryConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6676,
        )

        return self.__parent__._cast(_6676.PlanetaryConnectionDynamicAnalysis)

    @property
    def ring_pins_to_disc_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6683.RingPinsToDiscConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6683,
        )

        return self.__parent__._cast(_6683.RingPinsToDiscConnectionDynamicAnalysis)

    @property
    def rolling_ring_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6685.RollingRingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6685,
        )

        return self.__parent__._cast(_6685.RollingRingConnectionDynamicAnalysis)

    @property
    def shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6690.ShaftToMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6690,
        )

        return self.__parent__._cast(
            _6690.ShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6693.SpiralBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6693,
        )

        return self.__parent__._cast(_6693.SpiralBevelGearMeshDynamicAnalysis)

    @property
    def spring_damper_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6695.SpringDamperConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6695,
        )

        return self.__parent__._cast(_6695.SpringDamperConnectionDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6699.StraightBevelDiffGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6699,
        )

        return self.__parent__._cast(_6699.StraightBevelDiffGearMeshDynamicAnalysis)

    @property
    def straight_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6702.StraightBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6702,
        )

        return self.__parent__._cast(_6702.StraightBevelGearMeshDynamicAnalysis)

    @property
    def torque_converter_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6710.TorqueConverterConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6710,
        )

        return self.__parent__._cast(_6710.TorqueConverterConnectionDynamicAnalysis)

    @property
    def worm_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6717.WormGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6717,
        )

        return self.__parent__._cast(_6717.WormGearMeshDynamicAnalysis)

    @property
    def zerol_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6720.ZerolBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6720,
        )

        return self.__parent__._cast(_6720.ZerolBevelGearMeshDynamicAnalysis)

    @property
    def connection_dynamic_analysis(self: "CastSelf") -> "ConnectionDynamicAnalysis":
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
class ConnectionDynamicAnalysis(_7882.ConnectionFEAnalysis):
    """ConnectionDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2493.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

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
    def connection_design(self: "Self") -> "_2493.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

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
    def dynamic_analysis(self: "Self") -> "_6641.DynamicAnalysis":
        """mastapy.system_model.analyses_and_results.dynamic_analyses.DynamicAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionDynamicAnalysis
        """
        return _Cast_ConnectionDynamicAnalysis(self)
