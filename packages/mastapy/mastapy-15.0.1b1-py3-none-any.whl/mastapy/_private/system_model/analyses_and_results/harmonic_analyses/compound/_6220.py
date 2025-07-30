"""ConnectionCompoundHarmonicAnalysis"""

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

_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "ConnectionCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7885
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6005,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6188,
        _6190,
        _6194,
        _6197,
        _6202,
        _6207,
        _6209,
        _6212,
        _6215,
        _6218,
        _6223,
        _6225,
        _6229,
        _6231,
        _6233,
        _6239,
        _6244,
        _6248,
        _6250,
        _6252,
        _6255,
        _6258,
        _6268,
        _6270,
        _6277,
        _6280,
        _6284,
        _6287,
        _6290,
        _6293,
        _6296,
        _6305,
        _6311,
        _6314,
    )

    Self = TypeVar("Self", bound="ConnectionCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionCompoundHarmonicAnalysis._Cast_ConnectionCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionCompoundHarmonicAnalysis:
    """Special nested class for casting ConnectionCompoundHarmonicAnalysis to subclasses."""

    __parent__: "ConnectionCompoundHarmonicAnalysis"

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
    def abstract_shaft_to_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6188.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6188,
        )

        return self.__parent__._cast(
            _6188.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6190.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6190,
        )

        return self.__parent__._cast(
            _6190.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis
        )

    @property
    def belt_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6194.BeltConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6194,
        )

        return self.__parent__._cast(_6194.BeltConnectionCompoundHarmonicAnalysis)

    @property
    def bevel_differential_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6197.BevelDifferentialGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6197,
        )

        return self.__parent__._cast(
            _6197.BevelDifferentialGearMeshCompoundHarmonicAnalysis
        )

    @property
    def bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6202.BevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6202,
        )

        return self.__parent__._cast(_6202.BevelGearMeshCompoundHarmonicAnalysis)

    @property
    def clutch_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6207.ClutchConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6207,
        )

        return self.__parent__._cast(_6207.ClutchConnectionCompoundHarmonicAnalysis)

    @property
    def coaxial_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6209.CoaxialConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6209,
        )

        return self.__parent__._cast(_6209.CoaxialConnectionCompoundHarmonicAnalysis)

    @property
    def concept_coupling_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6212.ConceptCouplingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6212,
        )

        return self.__parent__._cast(
            _6212.ConceptCouplingConnectionCompoundHarmonicAnalysis
        )

    @property
    def concept_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6215.ConceptGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6215,
        )

        return self.__parent__._cast(_6215.ConceptGearMeshCompoundHarmonicAnalysis)

    @property
    def conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6218.ConicalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6218,
        )

        return self.__parent__._cast(_6218.ConicalGearMeshCompoundHarmonicAnalysis)

    @property
    def coupling_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6223.CouplingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6223,
        )

        return self.__parent__._cast(_6223.CouplingConnectionCompoundHarmonicAnalysis)

    @property
    def cvt_belt_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6225.CVTBeltConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6225,
        )

        return self.__parent__._cast(_6225.CVTBeltConnectionCompoundHarmonicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6229.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6229,
        )

        return self.__parent__._cast(
            _6229.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6231.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6231,
        )

        return self.__parent__._cast(
            _6231.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysis
        )

    @property
    def cylindrical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6233.CylindricalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6233,
        )

        return self.__parent__._cast(_6233.CylindricalGearMeshCompoundHarmonicAnalysis)

    @property
    def face_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6239.FaceGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6239,
        )

        return self.__parent__._cast(_6239.FaceGearMeshCompoundHarmonicAnalysis)

    @property
    def gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6244.GearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6244,
        )

        return self.__parent__._cast(_6244.GearMeshCompoundHarmonicAnalysis)

    @property
    def hypoid_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6248.HypoidGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6248,
        )

        return self.__parent__._cast(_6248.HypoidGearMeshCompoundHarmonicAnalysis)

    @property
    def inter_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6250.InterMountableComponentConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6250,
        )

        return self.__parent__._cast(
            _6250.InterMountableComponentConnectionCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6252.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6252,
        )

        return self.__parent__._cast(
            _6252.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6255.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6255,
        )

        return self.__parent__._cast(
            _6255.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6258.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6258,
        )

        return self.__parent__._cast(
            _6258.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6268.PartToPartShearCouplingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6268,
        )

        return self.__parent__._cast(
            _6268.PartToPartShearCouplingConnectionCompoundHarmonicAnalysis
        )

    @property
    def planetary_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6270.PlanetaryConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6270,
        )

        return self.__parent__._cast(_6270.PlanetaryConnectionCompoundHarmonicAnalysis)

    @property
    def ring_pins_to_disc_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6277.RingPinsToDiscConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6277,
        )

        return self.__parent__._cast(
            _6277.RingPinsToDiscConnectionCompoundHarmonicAnalysis
        )

    @property
    def rolling_ring_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6280.RollingRingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6280,
        )

        return self.__parent__._cast(
            _6280.RollingRingConnectionCompoundHarmonicAnalysis
        )

    @property
    def shaft_to_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6284.ShaftToMountableComponentConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6284,
        )

        return self.__parent__._cast(
            _6284.ShaftToMountableComponentConnectionCompoundHarmonicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6287.SpiralBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6287,
        )

        return self.__parent__._cast(_6287.SpiralBevelGearMeshCompoundHarmonicAnalysis)

    @property
    def spring_damper_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6290.SpringDamperConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6290,
        )

        return self.__parent__._cast(
            _6290.SpringDamperConnectionCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6293.StraightBevelDiffGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6293,
        )

        return self.__parent__._cast(
            _6293.StraightBevelDiffGearMeshCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6296.StraightBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6296,
        )

        return self.__parent__._cast(
            _6296.StraightBevelGearMeshCompoundHarmonicAnalysis
        )

    @property
    def torque_converter_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6305.TorqueConverterConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6305,
        )

        return self.__parent__._cast(
            _6305.TorqueConverterConnectionCompoundHarmonicAnalysis
        )

    @property
    def worm_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6311.WormGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6311,
        )

        return self.__parent__._cast(_6311.WormGearMeshCompoundHarmonicAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6314.ZerolBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6314,
        )

        return self.__parent__._cast(_6314.ZerolBevelGearMeshCompoundHarmonicAnalysis)

    @property
    def connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "ConnectionCompoundHarmonicAnalysis":
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
class ConnectionCompoundHarmonicAnalysis(_7881.ConnectionCompoundAnalysis):
    """ConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_COMPOUND_HARMONIC_ANALYSIS

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
    ) -> "List[_6005.ConnectionHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ConnectionHarmonicAnalysis]

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
    ) -> "List[_6005.ConnectionHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ConnectionHarmonicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ConnectionCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionCompoundHarmonicAnalysis
        """
        return _Cast_ConnectionCompoundHarmonicAnalysis(self)
