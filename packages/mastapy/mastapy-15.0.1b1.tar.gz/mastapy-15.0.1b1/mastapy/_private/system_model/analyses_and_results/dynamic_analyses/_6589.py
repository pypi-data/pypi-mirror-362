"""AbstractAssemblyDynamicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6672

_ABSTRACT_ASSEMBLY_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "AbstractAssemblyDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7889,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6595,
        _6596,
        _6599,
        _6602,
        _6607,
        _6609,
        _6611,
        _6616,
        _6620,
        _6623,
        _6627,
        _6630,
        _6632,
        _6638,
        _6646,
        _6648,
        _6651,
        _6655,
        _6659,
        _6662,
        _6665,
        _6668,
        _6674,
        _6677,
        _6684,
        _6687,
        _6691,
        _6694,
        _6696,
        _6700,
        _6703,
        _6706,
        _6711,
        _6718,
        _6721,
    )
    from mastapy._private.system_model.part_model import _2659

    Self = TypeVar("Self", bound="AbstractAssemblyDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractAssemblyDynamicAnalysis._Cast_AbstractAssemblyDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyDynamicAnalysis:
    """Special nested class for casting AbstractAssemblyDynamicAnalysis to subclasses."""

    __parent__: "AbstractAssemblyDynamicAnalysis"

    @property
    def part_dynamic_analysis(self: "CastSelf") -> "_6672.PartDynamicAnalysis":
        return self.__parent__._cast(_6672.PartDynamicAnalysis)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7889.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7889,
        )

        return self.__parent__._cast(_7889.PartFEAnalysis)

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
    def agma_gleason_conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6595.AGMAGleasonConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6595,
        )

        return self.__parent__._cast(_6595.AGMAGleasonConicalGearSetDynamicAnalysis)

    @property
    def assembly_dynamic_analysis(self: "CastSelf") -> "_6596.AssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6596,
        )

        return self.__parent__._cast(_6596.AssemblyDynamicAnalysis)

    @property
    def belt_drive_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6599.BeltDriveDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6599,
        )

        return self.__parent__._cast(_6599.BeltDriveDynamicAnalysis)

    @property
    def bevel_differential_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6602.BevelDifferentialGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6602,
        )

        return self.__parent__._cast(_6602.BevelDifferentialGearSetDynamicAnalysis)

    @property
    def bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6607.BevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6607,
        )

        return self.__parent__._cast(_6607.BevelGearSetDynamicAnalysis)

    @property
    def bolted_joint_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6609.BoltedJointDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6609,
        )

        return self.__parent__._cast(_6609.BoltedJointDynamicAnalysis)

    @property
    def clutch_dynamic_analysis(self: "CastSelf") -> "_6611.ClutchDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6611,
        )

        return self.__parent__._cast(_6611.ClutchDynamicAnalysis)

    @property
    def concept_coupling_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6616.ConceptCouplingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6616,
        )

        return self.__parent__._cast(_6616.ConceptCouplingDynamicAnalysis)

    @property
    def concept_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6620.ConceptGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6620,
        )

        return self.__parent__._cast(_6620.ConceptGearSetDynamicAnalysis)

    @property
    def conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6623.ConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6623,
        )

        return self.__parent__._cast(_6623.ConicalGearSetDynamicAnalysis)

    @property
    def coupling_dynamic_analysis(self: "CastSelf") -> "_6627.CouplingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6627,
        )

        return self.__parent__._cast(_6627.CouplingDynamicAnalysis)

    @property
    def cvt_dynamic_analysis(self: "CastSelf") -> "_6630.CVTDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6630,
        )

        return self.__parent__._cast(_6630.CVTDynamicAnalysis)

    @property
    def cycloidal_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6632.CycloidalAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6632,
        )

        return self.__parent__._cast(_6632.CycloidalAssemblyDynamicAnalysis)

    @property
    def cylindrical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6638.CylindricalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6638,
        )

        return self.__parent__._cast(_6638.CylindricalGearSetDynamicAnalysis)

    @property
    def face_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6646.FaceGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6646,
        )

        return self.__parent__._cast(_6646.FaceGearSetDynamicAnalysis)

    @property
    def flexible_pin_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6648.FlexiblePinAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6648,
        )

        return self.__parent__._cast(_6648.FlexiblePinAssemblyDynamicAnalysis)

    @property
    def gear_set_dynamic_analysis(self: "CastSelf") -> "_6651.GearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6651,
        )

        return self.__parent__._cast(_6651.GearSetDynamicAnalysis)

    @property
    def hypoid_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6655.HypoidGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6655,
        )

        return self.__parent__._cast(_6655.HypoidGearSetDynamicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6659.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6659,
        )

        return self.__parent__._cast(
            _6659.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6662.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6662,
        )

        return self.__parent__._cast(
            _6662.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6665.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6665,
        )

        return self.__parent__._cast(
            _6665.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis
        )

    @property
    def microphone_array_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6668.MicrophoneArrayDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6668,
        )

        return self.__parent__._cast(_6668.MicrophoneArrayDynamicAnalysis)

    @property
    def part_to_part_shear_coupling_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6674.PartToPartShearCouplingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6674,
        )

        return self.__parent__._cast(_6674.PartToPartShearCouplingDynamicAnalysis)

    @property
    def planetary_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6677.PlanetaryGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6677,
        )

        return self.__parent__._cast(_6677.PlanetaryGearSetDynamicAnalysis)

    @property
    def rolling_ring_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6684.RollingRingAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6684,
        )

        return self.__parent__._cast(_6684.RollingRingAssemblyDynamicAnalysis)

    @property
    def root_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6687.RootAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6687,
        )

        return self.__parent__._cast(_6687.RootAssemblyDynamicAnalysis)

    @property
    def specialised_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6691.SpecialisedAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6691,
        )

        return self.__parent__._cast(_6691.SpecialisedAssemblyDynamicAnalysis)

    @property
    def spiral_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6694.SpiralBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6694,
        )

        return self.__parent__._cast(_6694.SpiralBevelGearSetDynamicAnalysis)

    @property
    def spring_damper_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6696.SpringDamperDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6696,
        )

        return self.__parent__._cast(_6696.SpringDamperDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6700.StraightBevelDiffGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6700,
        )

        return self.__parent__._cast(_6700.StraightBevelDiffGearSetDynamicAnalysis)

    @property
    def straight_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6703.StraightBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6703,
        )

        return self.__parent__._cast(_6703.StraightBevelGearSetDynamicAnalysis)

    @property
    def synchroniser_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6706.SynchroniserDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6706,
        )

        return self.__parent__._cast(_6706.SynchroniserDynamicAnalysis)

    @property
    def torque_converter_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6711.TorqueConverterDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6711,
        )

        return self.__parent__._cast(_6711.TorqueConverterDynamicAnalysis)

    @property
    def worm_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6718.WormGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6718,
        )

        return self.__parent__._cast(_6718.WormGearSetDynamicAnalysis)

    @property
    def zerol_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6721.ZerolBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6721,
        )

        return self.__parent__._cast(_6721.ZerolBevelGearSetDynamicAnalysis)

    @property
    def abstract_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "AbstractAssemblyDynamicAnalysis":
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
class AbstractAssemblyDynamicAnalysis(_6672.PartDynamicAnalysis):
    """AbstractAssemblyDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_DYNAMIC_ANALYSIS

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
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyDynamicAnalysis
        """
        return _Cast_AbstractAssemblyDynamicAnalysis(self)
