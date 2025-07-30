"""SpecialisedAssemblyCompoundCriticalSpeedAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6993,
)

_SPECIALISED_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "SpecialisedAssemblyCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6962,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6999,
        _7003,
        _7006,
        _7011,
        _7013,
        _7014,
        _7019,
        _7024,
        _7027,
        _7030,
        _7034,
        _7036,
        _7042,
        _7048,
        _7050,
        _7053,
        _7057,
        _7061,
        _7064,
        _7067,
        _7070,
        _7074,
        _7075,
        _7079,
        _7086,
        _7096,
        _7097,
        _7102,
        _7105,
        _7108,
        _7112,
        _7120,
        _7123,
    )

    Self = TypeVar("Self", bound="SpecialisedAssemblyCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyCompoundCriticalSpeedAnalysis._Cast_SpecialisedAssemblyCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyCompoundCriticalSpeedAnalysis:
    """Special nested class for casting SpecialisedAssemblyCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "SpecialisedAssemblyCompoundCriticalSpeedAnalysis"

    @property
    def abstract_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6993.AbstractAssemblyCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(
            _6993.AbstractAssemblyCompoundCriticalSpeedAnalysis
        )

    @property
    def part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7074.PartCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7074,
        )

        return self.__parent__._cast(_7074.PartCompoundCriticalSpeedAnalysis)

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
    def agma_gleason_conical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6999.AGMAGleasonConicalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6999,
        )

        return self.__parent__._cast(
            _6999.AGMAGleasonConicalGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def belt_drive_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7003.BeltDriveCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7003,
        )

        return self.__parent__._cast(_7003.BeltDriveCompoundCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7006.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7006,
        )

        return self.__parent__._cast(
            _7006.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7011.BevelGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7011,
        )

        return self.__parent__._cast(_7011.BevelGearSetCompoundCriticalSpeedAnalysis)

    @property
    def bolted_joint_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7013.BoltedJointCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7013,
        )

        return self.__parent__._cast(_7013.BoltedJointCompoundCriticalSpeedAnalysis)

    @property
    def clutch_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7014.ClutchCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7014,
        )

        return self.__parent__._cast(_7014.ClutchCompoundCriticalSpeedAnalysis)

    @property
    def concept_coupling_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7019.ConceptCouplingCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7019,
        )

        return self.__parent__._cast(_7019.ConceptCouplingCompoundCriticalSpeedAnalysis)

    @property
    def concept_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7024.ConceptGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7024,
        )

        return self.__parent__._cast(_7024.ConceptGearSetCompoundCriticalSpeedAnalysis)

    @property
    def conical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7027.ConicalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7027,
        )

        return self.__parent__._cast(_7027.ConicalGearSetCompoundCriticalSpeedAnalysis)

    @property
    def coupling_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7030.CouplingCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7030,
        )

        return self.__parent__._cast(_7030.CouplingCompoundCriticalSpeedAnalysis)

    @property
    def cvt_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7034.CVTCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7034,
        )

        return self.__parent__._cast(_7034.CVTCompoundCriticalSpeedAnalysis)

    @property
    def cycloidal_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7036.CycloidalAssemblyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7036,
        )

        return self.__parent__._cast(
            _7036.CycloidalAssemblyCompoundCriticalSpeedAnalysis
        )

    @property
    def cylindrical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7042.CylindricalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7042,
        )

        return self.__parent__._cast(
            _7042.CylindricalGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def face_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7048.FaceGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7048,
        )

        return self.__parent__._cast(_7048.FaceGearSetCompoundCriticalSpeedAnalysis)

    @property
    def flexible_pin_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7050.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7050,
        )

        return self.__parent__._cast(
            _7050.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis
        )

    @property
    def gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7053.GearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7053,
        )

        return self.__parent__._cast(_7053.GearSetCompoundCriticalSpeedAnalysis)

    @property
    def hypoid_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7057.HypoidGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7057,
        )

        return self.__parent__._cast(_7057.HypoidGearSetCompoundCriticalSpeedAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7061.KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7061,
        )

        return self.__parent__._cast(
            _7061.KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7064.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7064,
        )

        return self.__parent__._cast(
            _7064.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> (
        "_7067.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7067,
        )

        return self.__parent__._cast(
            _7067.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def microphone_array_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7070.MicrophoneArrayCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7070,
        )

        return self.__parent__._cast(_7070.MicrophoneArrayCompoundCriticalSpeedAnalysis)

    @property
    def part_to_part_shear_coupling_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7075.PartToPartShearCouplingCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7075,
        )

        return self.__parent__._cast(
            _7075.PartToPartShearCouplingCompoundCriticalSpeedAnalysis
        )

    @property
    def planetary_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7079.PlanetaryGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7079,
        )

        return self.__parent__._cast(
            _7079.PlanetaryGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def rolling_ring_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7086.RollingRingAssemblyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7086,
        )

        return self.__parent__._cast(
            _7086.RollingRingAssemblyCompoundCriticalSpeedAnalysis
        )

    @property
    def spiral_bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7096.SpiralBevelGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7096,
        )

        return self.__parent__._cast(
            _7096.SpiralBevelGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def spring_damper_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7097.SpringDamperCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7097,
        )

        return self.__parent__._cast(_7097.SpringDamperCompoundCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7102.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7102,
        )

        return self.__parent__._cast(
            _7102.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7105.StraightBevelGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7105,
        )

        return self.__parent__._cast(
            _7105.StraightBevelGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def synchroniser_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7108.SynchroniserCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7108,
        )

        return self.__parent__._cast(_7108.SynchroniserCompoundCriticalSpeedAnalysis)

    @property
    def torque_converter_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7112.TorqueConverterCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7112,
        )

        return self.__parent__._cast(_7112.TorqueConverterCompoundCriticalSpeedAnalysis)

    @property
    def worm_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7120.WormGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7120,
        )

        return self.__parent__._cast(_7120.WormGearSetCompoundCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7123.ZerolBevelGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7123,
        )

        return self.__parent__._cast(
            _7123.ZerolBevelGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def specialised_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyCompoundCriticalSpeedAnalysis":
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
class SpecialisedAssemblyCompoundCriticalSpeedAnalysis(
    _6993.AbstractAssemblyCompoundCriticalSpeedAnalysis
):
    """SpecialisedAssemblyCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS

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
    ) -> "List[_6962.SpecialisedAssemblyCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.SpecialisedAssemblyCriticalSpeedAnalysis]

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
    ) -> "List[_6962.SpecialisedAssemblyCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.SpecialisedAssemblyCriticalSpeedAnalysis]

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
    ) -> "_Cast_SpecialisedAssemblyCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyCompoundCriticalSpeedAnalysis
        """
        return _Cast_SpecialisedAssemblyCompoundCriticalSpeedAnalysis(self)
