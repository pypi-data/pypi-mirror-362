"""ConnectionCompoundSystemDeflection"""

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

_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "ConnectionCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7885
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2968,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3097,
        _3099,
        _3103,
        _3106,
        _3111,
        _3116,
        _3118,
        _3121,
        _3124,
        _3127,
        _3132,
        _3134,
        _3138,
        _3140,
        _3142,
        _3149,
        _3154,
        _3158,
        _3160,
        _3162,
        _3165,
        _3168,
        _3178,
        _3180,
        _3187,
        _3190,
        _3195,
        _3198,
        _3201,
        _3204,
        _3207,
        _3216,
        _3222,
        _3225,
    )

    Self = TypeVar("Self", bound="ConnectionCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionCompoundSystemDeflection._Cast_ConnectionCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionCompoundSystemDeflection:
    """Special nested class for casting ConnectionCompoundSystemDeflection to subclasses."""

    __parent__: "ConnectionCompoundSystemDeflection"

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
    def abstract_shaft_to_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3097.AbstractShaftToMountableComponentConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3097,
        )

        return self.__parent__._cast(
            _3097.AbstractShaftToMountableComponentConnectionCompoundSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3099.AGMAGleasonConicalGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3099,
        )

        return self.__parent__._cast(
            _3099.AGMAGleasonConicalGearMeshCompoundSystemDeflection
        )

    @property
    def belt_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3103.BeltConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3103,
        )

        return self.__parent__._cast(_3103.BeltConnectionCompoundSystemDeflection)

    @property
    def bevel_differential_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3106.BevelDifferentialGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3106,
        )

        return self.__parent__._cast(
            _3106.BevelDifferentialGearMeshCompoundSystemDeflection
        )

    @property
    def bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3111.BevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3111,
        )

        return self.__parent__._cast(_3111.BevelGearMeshCompoundSystemDeflection)

    @property
    def clutch_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3116.ClutchConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3116,
        )

        return self.__parent__._cast(_3116.ClutchConnectionCompoundSystemDeflection)

    @property
    def coaxial_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3118.CoaxialConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3118,
        )

        return self.__parent__._cast(_3118.CoaxialConnectionCompoundSystemDeflection)

    @property
    def concept_coupling_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3121.ConceptCouplingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3121,
        )

        return self.__parent__._cast(
            _3121.ConceptCouplingConnectionCompoundSystemDeflection
        )

    @property
    def concept_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3124.ConceptGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3124,
        )

        return self.__parent__._cast(_3124.ConceptGearMeshCompoundSystemDeflection)

    @property
    def conical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3127.ConicalGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3127,
        )

        return self.__parent__._cast(_3127.ConicalGearMeshCompoundSystemDeflection)

    @property
    def coupling_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3132.CouplingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3132,
        )

        return self.__parent__._cast(_3132.CouplingConnectionCompoundSystemDeflection)

    @property
    def cvt_belt_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3134.CVTBeltConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3134,
        )

        return self.__parent__._cast(_3134.CVTBeltConnectionCompoundSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3138.CycloidalDiscCentralBearingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3138,
        )

        return self.__parent__._cast(
            _3138.CycloidalDiscCentralBearingConnectionCompoundSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3140.CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3140,
        )

        return self.__parent__._cast(
            _3140.CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection
        )

    @property
    def cylindrical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3142.CylindricalGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3142,
        )

        return self.__parent__._cast(_3142.CylindricalGearMeshCompoundSystemDeflection)

    @property
    def face_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3149.FaceGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3149,
        )

        return self.__parent__._cast(_3149.FaceGearMeshCompoundSystemDeflection)

    @property
    def gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3154.GearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3154,
        )

        return self.__parent__._cast(_3154.GearMeshCompoundSystemDeflection)

    @property
    def hypoid_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3158.HypoidGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3158,
        )

        return self.__parent__._cast(_3158.HypoidGearMeshCompoundSystemDeflection)

    @property
    def inter_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3160.InterMountableComponentConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3160,
        )

        return self.__parent__._cast(
            _3160.InterMountableComponentConnectionCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3162.KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3162,
        )

        return self.__parent__._cast(
            _3162.KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3165.KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3165,
        )

        return self.__parent__._cast(
            _3165.KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3168.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3168,
        )

        return self.__parent__._cast(
            _3168.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3178.PartToPartShearCouplingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3178,
        )

        return self.__parent__._cast(
            _3178.PartToPartShearCouplingConnectionCompoundSystemDeflection
        )

    @property
    def planetary_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3180.PlanetaryConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3180,
        )

        return self.__parent__._cast(_3180.PlanetaryConnectionCompoundSystemDeflection)

    @property
    def ring_pins_to_disc_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3187.RingPinsToDiscConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3187,
        )

        return self.__parent__._cast(
            _3187.RingPinsToDiscConnectionCompoundSystemDeflection
        )

    @property
    def rolling_ring_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3190.RollingRingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3190,
        )

        return self.__parent__._cast(
            _3190.RollingRingConnectionCompoundSystemDeflection
        )

    @property
    def shaft_to_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3195.ShaftToMountableComponentConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3195,
        )

        return self.__parent__._cast(
            _3195.ShaftToMountableComponentConnectionCompoundSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3198.SpiralBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3198,
        )

        return self.__parent__._cast(_3198.SpiralBevelGearMeshCompoundSystemDeflection)

    @property
    def spring_damper_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3201.SpringDamperConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3201,
        )

        return self.__parent__._cast(
            _3201.SpringDamperConnectionCompoundSystemDeflection
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3204.StraightBevelDiffGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3204,
        )

        return self.__parent__._cast(
            _3204.StraightBevelDiffGearMeshCompoundSystemDeflection
        )

    @property
    def straight_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3207.StraightBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3207,
        )

        return self.__parent__._cast(
            _3207.StraightBevelGearMeshCompoundSystemDeflection
        )

    @property
    def torque_converter_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3216.TorqueConverterConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3216,
        )

        return self.__parent__._cast(
            _3216.TorqueConverterConnectionCompoundSystemDeflection
        )

    @property
    def worm_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3222.WormGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3222,
        )

        return self.__parent__._cast(_3222.WormGearMeshCompoundSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3225.ZerolBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3225,
        )

        return self.__parent__._cast(_3225.ZerolBevelGearMeshCompoundSystemDeflection)

    @property
    def connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "ConnectionCompoundSystemDeflection":
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
class ConnectionCompoundSystemDeflection(_7881.ConnectionCompoundAnalysis):
    """ConnectionCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def energy_lost(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnergyLost")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def energy_lost_contribution(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnergyLostContribution")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_2968.ConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConnectionSystemDeflection]

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
    ) -> "List[_2968.ConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConnectionSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_ConnectionCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConnectionCompoundSystemDeflection
        """
        return _Cast_ConnectionCompoundSystemDeflection(self)
