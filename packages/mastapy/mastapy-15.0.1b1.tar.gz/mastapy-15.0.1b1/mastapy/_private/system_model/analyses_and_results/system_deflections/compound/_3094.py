"""AbstractAssemblyCompoundSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _3176,
)

_ABSTRACT_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "AbstractAssemblyCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2926,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3100,
        _3101,
        _3104,
        _3107,
        _3112,
        _3114,
        _3115,
        _3119,
        _3120,
        _3125,
        _3128,
        _3129,
        _3131,
        _3135,
        _3137,
        _3143,
        _3150,
        _3152,
        _3155,
        _3159,
        _3163,
        _3166,
        _3169,
        _3172,
        _3177,
        _3181,
        _3188,
        _3191,
        _3196,
        _3199,
        _3200,
        _3205,
        _3208,
        _3211,
        _3215,
        _3223,
        _3226,
    )

    Self = TypeVar("Self", bound="AbstractAssemblyCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractAssemblyCompoundSystemDeflection._Cast_AbstractAssemblyCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyCompoundSystemDeflection:
    """Special nested class for casting AbstractAssemblyCompoundSystemDeflection to subclasses."""

    __parent__: "AbstractAssemblyCompoundSystemDeflection"

    @property
    def part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3176.PartCompoundSystemDeflection":
        return self.__parent__._cast(_3176.PartCompoundSystemDeflection)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7888.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7888,
        )

        return self.__parent__._cast(_7888.PartCompoundAnalysis)

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
    def agma_gleason_conical_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3100.AGMAGleasonConicalGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3100,
        )

        return self.__parent__._cast(
            _3100.AGMAGleasonConicalGearSetCompoundSystemDeflection
        )

    @property
    def assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3101.AssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3101,
        )

        return self.__parent__._cast(_3101.AssemblyCompoundSystemDeflection)

    @property
    def belt_drive_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3104.BeltDriveCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3104,
        )

        return self.__parent__._cast(_3104.BeltDriveCompoundSystemDeflection)

    @property
    def bevel_differential_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3107.BevelDifferentialGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3107,
        )

        return self.__parent__._cast(
            _3107.BevelDifferentialGearSetCompoundSystemDeflection
        )

    @property
    def bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3112.BevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3112,
        )

        return self.__parent__._cast(_3112.BevelGearSetCompoundSystemDeflection)

    @property
    def bolted_joint_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3114.BoltedJointCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3114,
        )

        return self.__parent__._cast(_3114.BoltedJointCompoundSystemDeflection)

    @property
    def clutch_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3115.ClutchCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3115,
        )

        return self.__parent__._cast(_3115.ClutchCompoundSystemDeflection)

    @property
    def concept_coupling_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3120.ConceptCouplingCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3120,
        )

        return self.__parent__._cast(_3120.ConceptCouplingCompoundSystemDeflection)

    @property
    def concept_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3125.ConceptGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3125,
        )

        return self.__parent__._cast(_3125.ConceptGearSetCompoundSystemDeflection)

    @property
    def conical_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3128.ConicalGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3128,
        )

        return self.__parent__._cast(_3128.ConicalGearSetCompoundSystemDeflection)

    @property
    def coupling_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3131.CouplingCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3131,
        )

        return self.__parent__._cast(_3131.CouplingCompoundSystemDeflection)

    @property
    def cvt_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3135.CVTCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3135,
        )

        return self.__parent__._cast(_3135.CVTCompoundSystemDeflection)

    @property
    def cycloidal_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3137.CycloidalAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3137,
        )

        return self.__parent__._cast(_3137.CycloidalAssemblyCompoundSystemDeflection)

    @property
    def cylindrical_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3143.CylindricalGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3143,
        )

        return self.__parent__._cast(_3143.CylindricalGearSetCompoundSystemDeflection)

    @property
    def face_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3150.FaceGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3150,
        )

        return self.__parent__._cast(_3150.FaceGearSetCompoundSystemDeflection)

    @property
    def flexible_pin_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3152.FlexiblePinAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3152,
        )

        return self.__parent__._cast(_3152.FlexiblePinAssemblyCompoundSystemDeflection)

    @property
    def gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3155.GearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3155,
        )

        return self.__parent__._cast(_3155.GearSetCompoundSystemDeflection)

    @property
    def hypoid_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3159.HypoidGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3159,
        )

        return self.__parent__._cast(_3159.HypoidGearSetCompoundSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3163.KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3163,
        )

        return self.__parent__._cast(
            _3163.KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3166.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3166,
        )

        return self.__parent__._cast(
            _3166.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3169.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3169,
        )

        return self.__parent__._cast(
            _3169.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection
        )

    @property
    def microphone_array_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3172.MicrophoneArrayCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3172,
        )

        return self.__parent__._cast(_3172.MicrophoneArrayCompoundSystemDeflection)

    @property
    def part_to_part_shear_coupling_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3177.PartToPartShearCouplingCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3177,
        )

        return self.__parent__._cast(
            _3177.PartToPartShearCouplingCompoundSystemDeflection
        )

    @property
    def planetary_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3181.PlanetaryGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3181,
        )

        return self.__parent__._cast(_3181.PlanetaryGearSetCompoundSystemDeflection)

    @property
    def rolling_ring_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3188.RollingRingAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3188,
        )

        return self.__parent__._cast(_3188.RollingRingAssemblyCompoundSystemDeflection)

    @property
    def root_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3191.RootAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3191,
        )

        return self.__parent__._cast(_3191.RootAssemblyCompoundSystemDeflection)

    @property
    def specialised_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3196.SpecialisedAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3196,
        )

        return self.__parent__._cast(_3196.SpecialisedAssemblyCompoundSystemDeflection)

    @property
    def spiral_bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3199.SpiralBevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3199,
        )

        return self.__parent__._cast(_3199.SpiralBevelGearSetCompoundSystemDeflection)

    @property
    def spring_damper_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3200.SpringDamperCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3200,
        )

        return self.__parent__._cast(_3200.SpringDamperCompoundSystemDeflection)

    @property
    def straight_bevel_diff_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3205.StraightBevelDiffGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3205,
        )

        return self.__parent__._cast(
            _3205.StraightBevelDiffGearSetCompoundSystemDeflection
        )

    @property
    def straight_bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3208.StraightBevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3208,
        )

        return self.__parent__._cast(_3208.StraightBevelGearSetCompoundSystemDeflection)

    @property
    def synchroniser_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3211.SynchroniserCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3211,
        )

        return self.__parent__._cast(_3211.SynchroniserCompoundSystemDeflection)

    @property
    def torque_converter_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3215.TorqueConverterCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3215,
        )

        return self.__parent__._cast(_3215.TorqueConverterCompoundSystemDeflection)

    @property
    def worm_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3223.WormGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3223,
        )

        return self.__parent__._cast(_3223.WormGearSetCompoundSystemDeflection)

    @property
    def zerol_bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3226.ZerolBevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3226,
        )

        return self.__parent__._cast(_3226.ZerolBevelGearSetCompoundSystemDeflection)

    @property
    def abstract_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "AbstractAssemblyCompoundSystemDeflection":
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
class AbstractAssemblyCompoundSystemDeflection(_3176.PartCompoundSystemDeflection):
    """AbstractAssemblyCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def all_components(self: "Self") -> "List[_3119.ComponentCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.ComponentCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllComponents")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def all_connections(
        self: "Self",
    ) -> "List[_3129.ConnectionCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.ConnectionCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_2926.AbstractAssemblySystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.AbstractAssemblySystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_2926.AbstractAssemblySystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.AbstractAssemblySystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyCompoundSystemDeflection
        """
        return _Cast_AbstractAssemblyCompoundSystemDeflection(self)
