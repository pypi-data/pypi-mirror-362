"""AbstractAssemblyAdvancedSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
    _7479,
)

_ABSTRACT_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "AbstractAssemblyAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7401,
        _7402,
        _7405,
        _7408,
        _7413,
        _7415,
        _7416,
        _7421,
        _7426,
        _7429,
        _7433,
        _7436,
        _7439,
        _7445,
        _7452,
        _7454,
        _7457,
        _7461,
        _7465,
        _7468,
        _7471,
        _7476,
        _7480,
        _7484,
        _7492,
        _7494,
        _7498,
        _7501,
        _7502,
        _7507,
        _7510,
        _7513,
        _7517,
        _7526,
        _7529,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.part_model import _2659

    Self = TypeVar("Self", bound="AbstractAssemblyAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractAssemblyAdvancedSystemDeflection._Cast_AbstractAssemblyAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyAdvancedSystemDeflection:
    """Special nested class for casting AbstractAssemblyAdvancedSystemDeflection to subclasses."""

    __parent__: "AbstractAssemblyAdvancedSystemDeflection"

    @property
    def part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7479.PartAdvancedSystemDeflection":
        return self.__parent__._cast(_7479.PartAdvancedSystemDeflection)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7890.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7890,
        )

        return self.__parent__._cast(_7890.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7887.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7887,
        )

        return self.__parent__._cast(_7887.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

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
    def agma_gleason_conical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7401.AGMAGleasonConicalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7401,
        )

        return self.__parent__._cast(
            _7401.AGMAGleasonConicalGearSetAdvancedSystemDeflection
        )

    @property
    def assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7402.AssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7402,
        )

        return self.__parent__._cast(_7402.AssemblyAdvancedSystemDeflection)

    @property
    def belt_drive_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7405.BeltDriveAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7405,
        )

        return self.__parent__._cast(_7405.BeltDriveAdvancedSystemDeflection)

    @property
    def bevel_differential_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7408.BevelDifferentialGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7408,
        )

        return self.__parent__._cast(
            _7408.BevelDifferentialGearSetAdvancedSystemDeflection
        )

    @property
    def bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7413.BevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7413,
        )

        return self.__parent__._cast(_7413.BevelGearSetAdvancedSystemDeflection)

    @property
    def bolted_joint_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7415.BoltedJointAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7415,
        )

        return self.__parent__._cast(_7415.BoltedJointAdvancedSystemDeflection)

    @property
    def clutch_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7416.ClutchAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7416,
        )

        return self.__parent__._cast(_7416.ClutchAdvancedSystemDeflection)

    @property
    def concept_coupling_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7421.ConceptCouplingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7421,
        )

        return self.__parent__._cast(_7421.ConceptCouplingAdvancedSystemDeflection)

    @property
    def concept_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7426.ConceptGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7426,
        )

        return self.__parent__._cast(_7426.ConceptGearSetAdvancedSystemDeflection)

    @property
    def conical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7429.ConicalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7429,
        )

        return self.__parent__._cast(_7429.ConicalGearSetAdvancedSystemDeflection)

    @property
    def coupling_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7433.CouplingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7433,
        )

        return self.__parent__._cast(_7433.CouplingAdvancedSystemDeflection)

    @property
    def cvt_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7436.CVTAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7436,
        )

        return self.__parent__._cast(_7436.CVTAdvancedSystemDeflection)

    @property
    def cycloidal_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7439.CycloidalAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7439,
        )

        return self.__parent__._cast(_7439.CycloidalAssemblyAdvancedSystemDeflection)

    @property
    def cylindrical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7445.CylindricalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7445,
        )

        return self.__parent__._cast(_7445.CylindricalGearSetAdvancedSystemDeflection)

    @property
    def face_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7452.FaceGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7452,
        )

        return self.__parent__._cast(_7452.FaceGearSetAdvancedSystemDeflection)

    @property
    def flexible_pin_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7454.FlexiblePinAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7454,
        )

        return self.__parent__._cast(_7454.FlexiblePinAssemblyAdvancedSystemDeflection)

    @property
    def gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7457.GearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7457,
        )

        return self.__parent__._cast(_7457.GearSetAdvancedSystemDeflection)

    @property
    def hypoid_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7461.HypoidGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7461,
        )

        return self.__parent__._cast(_7461.HypoidGearSetAdvancedSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7465.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7465,
        )

        return self.__parent__._cast(
            _7465.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7468.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7468,
        )

        return self.__parent__._cast(
            _7468.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7471.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7471,
        )

        return self.__parent__._cast(
            _7471.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
        )

    @property
    def microphone_array_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7476.MicrophoneArrayAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7476,
        )

        return self.__parent__._cast(_7476.MicrophoneArrayAdvancedSystemDeflection)

    @property
    def part_to_part_shear_coupling_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7480.PartToPartShearCouplingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7480,
        )

        return self.__parent__._cast(
            _7480.PartToPartShearCouplingAdvancedSystemDeflection
        )

    @property
    def planetary_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7484.PlanetaryGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7484,
        )

        return self.__parent__._cast(_7484.PlanetaryGearSetAdvancedSystemDeflection)

    @property
    def rolling_ring_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7492.RollingRingAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7492,
        )

        return self.__parent__._cast(_7492.RollingRingAssemblyAdvancedSystemDeflection)

    @property
    def root_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7494.RootAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7494,
        )

        return self.__parent__._cast(_7494.RootAssemblyAdvancedSystemDeflection)

    @property
    def specialised_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7498.SpecialisedAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7498,
        )

        return self.__parent__._cast(_7498.SpecialisedAssemblyAdvancedSystemDeflection)

    @property
    def spiral_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7501.SpiralBevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7501,
        )

        return self.__parent__._cast(_7501.SpiralBevelGearSetAdvancedSystemDeflection)

    @property
    def spring_damper_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7502.SpringDamperAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7502,
        )

        return self.__parent__._cast(_7502.SpringDamperAdvancedSystemDeflection)

    @property
    def straight_bevel_diff_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7507.StraightBevelDiffGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7507,
        )

        return self.__parent__._cast(
            _7507.StraightBevelDiffGearSetAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7510.StraightBevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7510,
        )

        return self.__parent__._cast(_7510.StraightBevelGearSetAdvancedSystemDeflection)

    @property
    def synchroniser_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7513.SynchroniserAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7513,
        )

        return self.__parent__._cast(_7513.SynchroniserAdvancedSystemDeflection)

    @property
    def torque_converter_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7517.TorqueConverterAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7517,
        )

        return self.__parent__._cast(_7517.TorqueConverterAdvancedSystemDeflection)

    @property
    def worm_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7526.WormGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7526,
        )

        return self.__parent__._cast(_7526.WormGearSetAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7529.ZerolBevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7529,
        )

        return self.__parent__._cast(_7529.ZerolBevelGearSetAdvancedSystemDeflection)

    @property
    def abstract_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "AbstractAssemblyAdvancedSystemDeflection":
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
class AbstractAssemblyAdvancedSystemDeflection(_7479.PartAdvancedSystemDeflection):
    """AbstractAssemblyAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2659.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

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
    def assembly_design(self: "Self") -> "_2659.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyAdvancedSystemDeflection
        """
        return _Cast_AbstractAssemblyAdvancedSystemDeflection(self)
