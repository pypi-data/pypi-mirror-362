"""ConicalGearMeshCompoundAdvancedSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7589,
)

_CONICAL_GEAR_MESH_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "ConicalGearMeshCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7428,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7535,
        _7542,
        _7547,
        _7565,
        _7593,
        _7595,
        _7597,
        _7600,
        _7603,
        _7632,
        _7638,
        _7641,
        _7659,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )

    Self = TypeVar("Self", bound="ConicalGearMeshCompoundAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearMeshCompoundAdvancedSystemDeflection._Cast_ConicalGearMeshCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshCompoundAdvancedSystemDeflection:
    """Special nested class for casting ConicalGearMeshCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "ConicalGearMeshCompoundAdvancedSystemDeflection"

    @property
    def gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7589.GearMeshCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(_7589.GearMeshCompoundAdvancedSystemDeflection)

    @property
    def inter_mountable_component_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7595.InterMountableComponentConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7595,
        )

        return self.__parent__._cast(
            _7595.InterMountableComponentConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7565.ConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7565,
        )

        return self.__parent__._cast(_7565.ConnectionCompoundAdvancedSystemDeflection)

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
    def agma_gleason_conical_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7535.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7535,
        )

        return self.__parent__._cast(
            _7535.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_differential_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7542.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7542,
        )

        return self.__parent__._cast(
            _7542.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7547.BevelGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7547,
        )

        return self.__parent__._cast(
            _7547.BevelGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def hypoid_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7593.HypoidGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7593,
        )

        return self.__parent__._cast(
            _7593.HypoidGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> (
        "_7597.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7597,
        )

        return self.__parent__._cast(
            _7597.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7600.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7600,
        )

        return self.__parent__._cast(
            _7600.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7603.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7603,
        )

        return self.__parent__._cast(
            _7603.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7632.SpiralBevelGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7632,
        )

        return self.__parent__._cast(
            _7632.SpiralBevelGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7638.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7638,
        )

        return self.__parent__._cast(
            _7638.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7641.StraightBevelGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7641,
        )

        return self.__parent__._cast(
            _7641.StraightBevelGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def zerol_bevel_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7659.ZerolBevelGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7659,
        )

        return self.__parent__._cast(
            _7659.ZerolBevelGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def conical_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "ConicalGearMeshCompoundAdvancedSystemDeflection":
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
class ConicalGearMeshCompoundAdvancedSystemDeflection(
    _7589.GearMeshCompoundAdvancedSystemDeflection
):
    """ConicalGearMeshCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def planetaries(
        self: "Self",
    ) -> "List[ConicalGearMeshCompoundAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConicalGearMeshCompoundAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_7428.ConicalGearMeshAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearMeshAdvancedSystemDeflection]

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
    ) -> "List[_7428.ConicalGearMeshAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearMeshAdvancedSystemDeflection]

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
    ) -> "_Cast_ConicalGearMeshCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshCompoundAdvancedSystemDeflection
        """
        return _Cast_ConicalGearMeshCompoundAdvancedSystemDeflection(self)
