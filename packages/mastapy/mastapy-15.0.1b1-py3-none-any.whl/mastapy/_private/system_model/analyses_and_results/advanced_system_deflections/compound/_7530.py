"""AbstractAssemblyCompoundAdvancedSystemDeflection"""

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
    _7611,
)

_ABSTRACT_ASSEMBLY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "AbstractAssemblyCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7392,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7536,
        _7537,
        _7540,
        _7543,
        _7548,
        _7550,
        _7551,
        _7556,
        _7561,
        _7564,
        _7567,
        _7571,
        _7573,
        _7579,
        _7585,
        _7587,
        _7590,
        _7594,
        _7598,
        _7601,
        _7604,
        _7607,
        _7612,
        _7616,
        _7623,
        _7626,
        _7630,
        _7633,
        _7634,
        _7639,
        _7642,
        _7645,
        _7649,
        _7657,
        _7660,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )

    Self = TypeVar("Self", bound="AbstractAssemblyCompoundAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyCompoundAdvancedSystemDeflection:
    """Special nested class for casting AbstractAssemblyCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "AbstractAssemblyCompoundAdvancedSystemDeflection"

    @property
    def part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7611.PartCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(_7611.PartCompoundAdvancedSystemDeflection)

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
    def agma_gleason_conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7536.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7536,
        )

        return self.__parent__._cast(
            _7536.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7537.AssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7537,
        )

        return self.__parent__._cast(_7537.AssemblyCompoundAdvancedSystemDeflection)

    @property
    def belt_drive_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7540.BeltDriveCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7540,
        )

        return self.__parent__._cast(_7540.BeltDriveCompoundAdvancedSystemDeflection)

    @property
    def bevel_differential_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7543.BevelDifferentialGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7543,
        )

        return self.__parent__._cast(
            _7543.BevelDifferentialGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7548.BevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7548,
        )

        return self.__parent__._cast(_7548.BevelGearSetCompoundAdvancedSystemDeflection)

    @property
    def bolted_joint_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7550.BoltedJointCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7550,
        )

        return self.__parent__._cast(_7550.BoltedJointCompoundAdvancedSystemDeflection)

    @property
    def clutch_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7551.ClutchCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7551,
        )

        return self.__parent__._cast(_7551.ClutchCompoundAdvancedSystemDeflection)

    @property
    def concept_coupling_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7556.ConceptCouplingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7556,
        )

        return self.__parent__._cast(
            _7556.ConceptCouplingCompoundAdvancedSystemDeflection
        )

    @property
    def concept_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7561.ConceptGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7561,
        )

        return self.__parent__._cast(
            _7561.ConceptGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7564.ConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7564,
        )

        return self.__parent__._cast(
            _7564.ConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def coupling_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7567.CouplingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7567,
        )

        return self.__parent__._cast(_7567.CouplingCompoundAdvancedSystemDeflection)

    @property
    def cvt_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7571.CVTCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7571,
        )

        return self.__parent__._cast(_7571.CVTCompoundAdvancedSystemDeflection)

    @property
    def cycloidal_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7573.CycloidalAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7573,
        )

        return self.__parent__._cast(
            _7573.CycloidalAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def cylindrical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7579.CylindricalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7579,
        )

        return self.__parent__._cast(
            _7579.CylindricalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def face_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7585.FaceGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7585,
        )

        return self.__parent__._cast(_7585.FaceGearSetCompoundAdvancedSystemDeflection)

    @property
    def flexible_pin_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7587.FlexiblePinAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7587,
        )

        return self.__parent__._cast(
            _7587.FlexiblePinAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7590.GearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7590,
        )

        return self.__parent__._cast(_7590.GearSetCompoundAdvancedSystemDeflection)

    @property
    def hypoid_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7594.HypoidGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7594,
        )

        return self.__parent__._cast(
            _7594.HypoidGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7598.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7598,
        )

        return self.__parent__._cast(
            _7598.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7601.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7601,
        )

        return self.__parent__._cast(
            _7601.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7604.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7604,
        )

        return self.__parent__._cast(
            _7604.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def microphone_array_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7607.MicrophoneArrayCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7607,
        )

        return self.__parent__._cast(
            _7607.MicrophoneArrayCompoundAdvancedSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7612.PartToPartShearCouplingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7612,
        )

        return self.__parent__._cast(
            _7612.PartToPartShearCouplingCompoundAdvancedSystemDeflection
        )

    @property
    def planetary_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7616.PlanetaryGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7616,
        )

        return self.__parent__._cast(
            _7616.PlanetaryGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def rolling_ring_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7623.RollingRingAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7623,
        )

        return self.__parent__._cast(
            _7623.RollingRingAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def root_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7626.RootAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7626,
        )

        return self.__parent__._cast(_7626.RootAssemblyCompoundAdvancedSystemDeflection)

    @property
    def specialised_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7630.SpecialisedAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7630,
        )

        return self.__parent__._cast(
            _7630.SpecialisedAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def spiral_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7633.SpiralBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7633,
        )

        return self.__parent__._cast(
            _7633.SpiralBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def spring_damper_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7634.SpringDamperCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7634,
        )

        return self.__parent__._cast(_7634.SpringDamperCompoundAdvancedSystemDeflection)

    @property
    def straight_bevel_diff_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7639.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7639,
        )

        return self.__parent__._cast(
            _7639.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7642.StraightBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7642,
        )

        return self.__parent__._cast(
            _7642.StraightBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def synchroniser_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7645.SynchroniserCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7645,
        )

        return self.__parent__._cast(_7645.SynchroniserCompoundAdvancedSystemDeflection)

    @property
    def torque_converter_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7649.TorqueConverterCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7649,
        )

        return self.__parent__._cast(
            _7649.TorqueConverterCompoundAdvancedSystemDeflection
        )

    @property
    def worm_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7657.WormGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7657,
        )

        return self.__parent__._cast(_7657.WormGearSetCompoundAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7660.ZerolBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7660,
        )

        return self.__parent__._cast(
            _7660.ZerolBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def abstract_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "AbstractAssemblyCompoundAdvancedSystemDeflection":
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
class AbstractAssemblyCompoundAdvancedSystemDeflection(
    _7611.PartCompoundAdvancedSystemDeflection
):
    """AbstractAssemblyCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_7392.AbstractAssemblyAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection]

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
    ) -> "List[_7392.AbstractAssemblyAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractAssemblyCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyCompoundAdvancedSystemDeflection
        """
        return _Cast_AbstractAssemblyCompoundAdvancedSystemDeflection(self)
