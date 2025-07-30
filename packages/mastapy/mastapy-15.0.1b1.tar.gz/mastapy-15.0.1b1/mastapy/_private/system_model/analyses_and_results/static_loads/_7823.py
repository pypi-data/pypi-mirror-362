"""SpecialisedAssemblyLoadCase"""

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
from mastapy._private.system_model.analyses_and_results.static_loads import _7675

_SPECIALISED_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpecialisedAssemblyLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7684,
        _7690,
        _7693,
        _7698,
        _7699,
        _7703,
        _7709,
        _7712,
        _7717,
        _7722,
        _7724,
        _7726,
        _7734,
        _7755,
        _7757,
        _7764,
        _7776,
        _7783,
        _7786,
        _7789,
        _7793,
        _7799,
        _7802,
        _7804,
        _7816,
        _7826,
        _7829,
        _7832,
        _7835,
        _7839,
        _7845,
        _7856,
        _7859,
    )
    from mastapy._private.system_model.part_model import _2708

    Self = TypeVar("Self", bound="SpecialisedAssemblyLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyLoadCase._Cast_SpecialisedAssemblyLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyLoadCase:
    """Special nested class for casting SpecialisedAssemblyLoadCase to subclasses."""

    __parent__: "SpecialisedAssemblyLoadCase"

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_7675.AbstractAssemblyLoadCase":
        return self.__parent__._cast(_7675.AbstractAssemblyLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7799.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7799,
        )

        return self.__parent__._cast(_7799.PartLoadCase)

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
    def agma_gleason_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7684.AGMAGleasonConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7684,
        )

        return self.__parent__._cast(_7684.AGMAGleasonConicalGearSetLoadCase)

    @property
    def belt_drive_load_case(self: "CastSelf") -> "_7690.BeltDriveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7690,
        )

        return self.__parent__._cast(_7690.BeltDriveLoadCase)

    @property
    def bevel_differential_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7693.BevelDifferentialGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7693,
        )

        return self.__parent__._cast(_7693.BevelDifferentialGearSetLoadCase)

    @property
    def bevel_gear_set_load_case(self: "CastSelf") -> "_7698.BevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7698,
        )

        return self.__parent__._cast(_7698.BevelGearSetLoadCase)

    @property
    def bolted_joint_load_case(self: "CastSelf") -> "_7699.BoltedJointLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7699,
        )

        return self.__parent__._cast(_7699.BoltedJointLoadCase)

    @property
    def clutch_load_case(self: "CastSelf") -> "_7703.ClutchLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7703,
        )

        return self.__parent__._cast(_7703.ClutchLoadCase)

    @property
    def concept_coupling_load_case(self: "CastSelf") -> "_7709.ConceptCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7709,
        )

        return self.__parent__._cast(_7709.ConceptCouplingLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_7712.ConceptGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConceptGearSetLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_7717.ConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7717,
        )

        return self.__parent__._cast(_7717.ConicalGearSetLoadCase)

    @property
    def coupling_load_case(self: "CastSelf") -> "_7722.CouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7722,
        )

        return self.__parent__._cast(_7722.CouplingLoadCase)

    @property
    def cvt_load_case(self: "CastSelf") -> "_7724.CVTLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7724,
        )

        return self.__parent__._cast(_7724.CVTLoadCase)

    @property
    def cycloidal_assembly_load_case(
        self: "CastSelf",
    ) -> "_7726.CycloidalAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7726,
        )

        return self.__parent__._cast(_7726.CycloidalAssemblyLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7734.CylindricalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7734,
        )

        return self.__parent__._cast(_7734.CylindricalGearSetLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_7755.FaceGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7755,
        )

        return self.__parent__._cast(_7755.FaceGearSetLoadCase)

    @property
    def flexible_pin_assembly_load_case(
        self: "CastSelf",
    ) -> "_7757.FlexiblePinAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7757,
        )

        return self.__parent__._cast(_7757.FlexiblePinAssemblyLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7764.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7764,
        )

        return self.__parent__._cast(_7764.GearSetLoadCase)

    @property
    def hypoid_gear_set_load_case(self: "CastSelf") -> "_7776.HypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7776,
        )

        return self.__parent__._cast(_7776.HypoidGearSetLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7783.KlingelnbergCycloPalloidConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7783,
        )

        return self.__parent__._cast(
            _7783.KlingelnbergCycloPalloidConicalGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7786,
        )

        return self.__parent__._cast(
            _7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7789.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7789,
        )

        return self.__parent__._cast(
            _7789.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        )

    @property
    def microphone_array_load_case(self: "CastSelf") -> "_7793.MicrophoneArrayLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7793,
        )

        return self.__parent__._cast(_7793.MicrophoneArrayLoadCase)

    @property
    def part_to_part_shear_coupling_load_case(
        self: "CastSelf",
    ) -> "_7802.PartToPartShearCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7802,
        )

        return self.__parent__._cast(_7802.PartToPartShearCouplingLoadCase)

    @property
    def planetary_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7804.PlanetaryGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7804,
        )

        return self.__parent__._cast(_7804.PlanetaryGearSetLoadCase)

    @property
    def rolling_ring_assembly_load_case(
        self: "CastSelf",
    ) -> "_7816.RollingRingAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7816,
        )

        return self.__parent__._cast(_7816.RollingRingAssemblyLoadCase)

    @property
    def spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7826.SpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7826,
        )

        return self.__parent__._cast(_7826.SpiralBevelGearSetLoadCase)

    @property
    def spring_damper_load_case(self: "CastSelf") -> "_7829.SpringDamperLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7829,
        )

        return self.__parent__._cast(_7829.SpringDamperLoadCase)

    @property
    def straight_bevel_diff_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7832.StraightBevelDiffGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7832,
        )

        return self.__parent__._cast(_7832.StraightBevelDiffGearSetLoadCase)

    @property
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7835.StraightBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7835,
        )

        return self.__parent__._cast(_7835.StraightBevelGearSetLoadCase)

    @property
    def synchroniser_load_case(self: "CastSelf") -> "_7839.SynchroniserLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7839,
        )

        return self.__parent__._cast(_7839.SynchroniserLoadCase)

    @property
    def torque_converter_load_case(self: "CastSelf") -> "_7845.TorqueConverterLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7845,
        )

        return self.__parent__._cast(_7845.TorqueConverterLoadCase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_7856.WormGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7856,
        )

        return self.__parent__._cast(_7856.WormGearSetLoadCase)

    @property
    def zerol_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7859.ZerolBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7859,
        )

        return self.__parent__._cast(_7859.ZerolBevelGearSetLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyLoadCase":
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
class SpecialisedAssemblyLoadCase(_7675.AbstractAssemblyLoadCase):
    """SpecialisedAssemblyLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2708.SpecialisedAssembly":
        """mastapy.system_model.part_model.SpecialisedAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssemblyLoadCase":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyLoadCase
        """
        return _Cast_SpecialisedAssemblyLoadCase(self)
