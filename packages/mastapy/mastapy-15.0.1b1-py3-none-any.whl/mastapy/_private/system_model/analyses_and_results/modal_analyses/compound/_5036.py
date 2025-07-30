"""ConnectionCompoundModalAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7881

_CONNECTION_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "ConnectionCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7885
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4877
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _5004,
        _5006,
        _5010,
        _5013,
        _5018,
        _5023,
        _5025,
        _5028,
        _5031,
        _5034,
        _5039,
        _5041,
        _5045,
        _5047,
        _5049,
        _5055,
        _5060,
        _5064,
        _5066,
        _5068,
        _5071,
        _5074,
        _5084,
        _5086,
        _5093,
        _5096,
        _5100,
        _5103,
        _5106,
        _5109,
        _5112,
        _5121,
        _5127,
        _5130,
    )

    Self = TypeVar("Self", bound="ConnectionCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionCompoundModalAnalysis._Cast_ConnectionCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionCompoundModalAnalysis:
    """Special nested class for casting ConnectionCompoundModalAnalysis to subclasses."""

    __parent__: "ConnectionCompoundModalAnalysis"

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7881.ConnectionCompoundAnalysis":
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
    def abstract_shaft_to_mountable_component_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5004.AbstractShaftToMountableComponentConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5004,
        )

        return self.__parent__._cast(
            _5004.AbstractShaftToMountableComponentConnectionCompoundModalAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5006.AGMAGleasonConicalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5006,
        )

        return self.__parent__._cast(
            _5006.AGMAGleasonConicalGearMeshCompoundModalAnalysis
        )

    @property
    def belt_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5010.BeltConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5010,
        )

        return self.__parent__._cast(_5010.BeltConnectionCompoundModalAnalysis)

    @property
    def bevel_differential_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5013.BevelDifferentialGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5013,
        )

        return self.__parent__._cast(
            _5013.BevelDifferentialGearMeshCompoundModalAnalysis
        )

    @property
    def bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5018.BevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5018,
        )

        return self.__parent__._cast(_5018.BevelGearMeshCompoundModalAnalysis)

    @property
    def clutch_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5023.ClutchConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5023,
        )

        return self.__parent__._cast(_5023.ClutchConnectionCompoundModalAnalysis)

    @property
    def coaxial_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5025.CoaxialConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5025,
        )

        return self.__parent__._cast(_5025.CoaxialConnectionCompoundModalAnalysis)

    @property
    def concept_coupling_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5028.ConceptCouplingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5028,
        )

        return self.__parent__._cast(
            _5028.ConceptCouplingConnectionCompoundModalAnalysis
        )

    @property
    def concept_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5031.ConceptGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5031,
        )

        return self.__parent__._cast(_5031.ConceptGearMeshCompoundModalAnalysis)

    @property
    def conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5034.ConicalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5034,
        )

        return self.__parent__._cast(_5034.ConicalGearMeshCompoundModalAnalysis)

    @property
    def coupling_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5039.CouplingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5039,
        )

        return self.__parent__._cast(_5039.CouplingConnectionCompoundModalAnalysis)

    @property
    def cvt_belt_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5041.CVTBeltConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5041,
        )

        return self.__parent__._cast(_5041.CVTBeltConnectionCompoundModalAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5045.CycloidalDiscCentralBearingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5045,
        )

        return self.__parent__._cast(
            _5045.CycloidalDiscCentralBearingConnectionCompoundModalAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5047.CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5047,
        )

        return self.__parent__._cast(
            _5047.CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysis
        )

    @property
    def cylindrical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5049.CylindricalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5049,
        )

        return self.__parent__._cast(_5049.CylindricalGearMeshCompoundModalAnalysis)

    @property
    def face_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5055.FaceGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5055,
        )

        return self.__parent__._cast(_5055.FaceGearMeshCompoundModalAnalysis)

    @property
    def gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5060.GearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5060,
        )

        return self.__parent__._cast(_5060.GearMeshCompoundModalAnalysis)

    @property
    def hypoid_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5064.HypoidGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5064,
        )

        return self.__parent__._cast(_5064.HypoidGearMeshCompoundModalAnalysis)

    @property
    def inter_mountable_component_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5066.InterMountableComponentConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5066,
        )

        return self.__parent__._cast(
            _5066.InterMountableComponentConnectionCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5068.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5068,
        )

        return self.__parent__._cast(
            _5068.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5071.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5071,
        )

        return self.__parent__._cast(
            _5071.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5074.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5074,
        )

        return self.__parent__._cast(
            _5074.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5084.PartToPartShearCouplingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5084,
        )

        return self.__parent__._cast(
            _5084.PartToPartShearCouplingConnectionCompoundModalAnalysis
        )

    @property
    def planetary_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5086.PlanetaryConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5086,
        )

        return self.__parent__._cast(_5086.PlanetaryConnectionCompoundModalAnalysis)

    @property
    def ring_pins_to_disc_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5093.RingPinsToDiscConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5093,
        )

        return self.__parent__._cast(
            _5093.RingPinsToDiscConnectionCompoundModalAnalysis
        )

    @property
    def rolling_ring_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5096.RollingRingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5096,
        )

        return self.__parent__._cast(_5096.RollingRingConnectionCompoundModalAnalysis)

    @property
    def shaft_to_mountable_component_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5100.ShaftToMountableComponentConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5100,
        )

        return self.__parent__._cast(
            _5100.ShaftToMountableComponentConnectionCompoundModalAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5103.SpiralBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5103,
        )

        return self.__parent__._cast(_5103.SpiralBevelGearMeshCompoundModalAnalysis)

    @property
    def spring_damper_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5106.SpringDamperConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5106,
        )

        return self.__parent__._cast(_5106.SpringDamperConnectionCompoundModalAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5109.StraightBevelDiffGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5109,
        )

        return self.__parent__._cast(
            _5109.StraightBevelDiffGearMeshCompoundModalAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5112.StraightBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5112,
        )

        return self.__parent__._cast(_5112.StraightBevelGearMeshCompoundModalAnalysis)

    @property
    def torque_converter_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5121.TorqueConverterConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5121,
        )

        return self.__parent__._cast(
            _5121.TorqueConverterConnectionCompoundModalAnalysis
        )

    @property
    def worm_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5127.WormGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5127,
        )

        return self.__parent__._cast(_5127.WormGearMeshCompoundModalAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5130.ZerolBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5130,
        )

        return self.__parent__._cast(_5130.ZerolBevelGearMeshCompoundModalAnalysis)

    @property
    def connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "ConnectionCompoundModalAnalysis":
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
class ConnectionCompoundModalAnalysis(_7881.ConnectionCompoundAnalysis):
    """ConnectionCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_COMPOUND_MODAL_ANALYSIS

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
    ) -> "List[_4877.ConnectionModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ConnectionModalAnalysis]

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
    ) -> "List[_4877.ConnectionModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ConnectionModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ConnectionCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionCompoundModalAnalysis
        """
        return _Cast_ConnectionCompoundModalAnalysis(self)
