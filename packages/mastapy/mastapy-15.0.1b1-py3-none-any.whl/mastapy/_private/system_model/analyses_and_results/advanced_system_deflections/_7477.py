"""MountableComponentAdvancedSystemDeflection"""

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
    _7420,
)

_MOUNTABLE_COMPONENT_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "MountableComponentAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7399,
        _7403,
        _7406,
        _7409,
        _7410,
        _7411,
        _7418,
        _7423,
        _7424,
        _7427,
        _7431,
        _7435,
        _7438,
        _7443,
        _7447,
        _7450,
        _7455,
        _7459,
        _7463,
        _7466,
        _7469,
        _7473,
        _7474,
        _7478,
        _7479,
        _7482,
        _7485,
        _7486,
        _7487,
        _7488,
        _7489,
        _7491,
        _7496,
        _7499,
        _7504,
        _7505,
        _7508,
        _7511,
        _7512,
        _7514,
        _7515,
        _7516,
        _7519,
        _7520,
        _7522,
        _7523,
        _7524,
        _7527,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.part_model import _2693

    Self = TypeVar("Self", bound="MountableComponentAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentAdvancedSystemDeflection._Cast_MountableComponentAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentAdvancedSystemDeflection:
    """Special nested class for casting MountableComponentAdvancedSystemDeflection to subclasses."""

    __parent__: "MountableComponentAdvancedSystemDeflection"

    @property
    def component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7420.ComponentAdvancedSystemDeflection":
        return self.__parent__._cast(_7420.ComponentAdvancedSystemDeflection)

    @property
    def part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7479.PartAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7479,
        )

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
    def agma_gleason_conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7399.AGMAGleasonConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7399,
        )

        return self.__parent__._cast(
            _7399.AGMAGleasonConicalGearAdvancedSystemDeflection
        )

    @property
    def bearing_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7403.BearingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7403,
        )

        return self.__parent__._cast(_7403.BearingAdvancedSystemDeflection)

    @property
    def bevel_differential_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7406.BevelDifferentialGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7406,
        )

        return self.__parent__._cast(
            _7406.BevelDifferentialGearAdvancedSystemDeflection
        )

    @property
    def bevel_differential_planet_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7409.BevelDifferentialPlanetGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7409,
        )

        return self.__parent__._cast(
            _7409.BevelDifferentialPlanetGearAdvancedSystemDeflection
        )

    @property
    def bevel_differential_sun_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7410.BevelDifferentialSunGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7410,
        )

        return self.__parent__._cast(
            _7410.BevelDifferentialSunGearAdvancedSystemDeflection
        )

    @property
    def bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7411.BevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7411,
        )

        return self.__parent__._cast(_7411.BevelGearAdvancedSystemDeflection)

    @property
    def clutch_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7418.ClutchHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7418,
        )

        return self.__parent__._cast(_7418.ClutchHalfAdvancedSystemDeflection)

    @property
    def concept_coupling_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7423.ConceptCouplingHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7423,
        )

        return self.__parent__._cast(_7423.ConceptCouplingHalfAdvancedSystemDeflection)

    @property
    def concept_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7424.ConceptGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7424,
        )

        return self.__parent__._cast(_7424.ConceptGearAdvancedSystemDeflection)

    @property
    def conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7427.ConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7427,
        )

        return self.__parent__._cast(_7427.ConicalGearAdvancedSystemDeflection)

    @property
    def connector_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7431.ConnectorAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7431,
        )

        return self.__parent__._cast(_7431.ConnectorAdvancedSystemDeflection)

    @property
    def coupling_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7435.CouplingHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7435,
        )

        return self.__parent__._cast(_7435.CouplingHalfAdvancedSystemDeflection)

    @property
    def cvt_pulley_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7438.CVTPulleyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7438,
        )

        return self.__parent__._cast(_7438.CVTPulleyAdvancedSystemDeflection)

    @property
    def cylindrical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7443.CylindricalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7443,
        )

        return self.__parent__._cast(_7443.CylindricalGearAdvancedSystemDeflection)

    @property
    def cylindrical_planet_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7447.CylindricalPlanetGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7447,
        )

        return self.__parent__._cast(
            _7447.CylindricalPlanetGearAdvancedSystemDeflection
        )

    @property
    def face_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7450.FaceGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7450,
        )

        return self.__parent__._cast(_7450.FaceGearAdvancedSystemDeflection)

    @property
    def gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7455.GearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7455,
        )

        return self.__parent__._cast(_7455.GearAdvancedSystemDeflection)

    @property
    def hypoid_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7459.HypoidGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7459,
        )

        return self.__parent__._cast(_7459.HypoidGearAdvancedSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7463.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7463,
        )

        return self.__parent__._cast(
            _7463.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7466.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7466,
        )

        return self.__parent__._cast(
            _7466.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7469.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7469,
        )

        return self.__parent__._cast(
            _7469.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
        )

    @property
    def mass_disc_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7473.MassDiscAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7473,
        )

        return self.__parent__._cast(_7473.MassDiscAdvancedSystemDeflection)

    @property
    def measurement_component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7474.MeasurementComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7474,
        )

        return self.__parent__._cast(_7474.MeasurementComponentAdvancedSystemDeflection)

    @property
    def oil_seal_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7478.OilSealAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7478,
        )

        return self.__parent__._cast(_7478.OilSealAdvancedSystemDeflection)

    @property
    def part_to_part_shear_coupling_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7482.PartToPartShearCouplingHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7482,
        )

        return self.__parent__._cast(
            _7482.PartToPartShearCouplingHalfAdvancedSystemDeflection
        )

    @property
    def planet_carrier_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7485.PlanetCarrierAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7485,
        )

        return self.__parent__._cast(_7485.PlanetCarrierAdvancedSystemDeflection)

    @property
    def point_load_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7486.PointLoadAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7486,
        )

        return self.__parent__._cast(_7486.PointLoadAdvancedSystemDeflection)

    @property
    def power_load_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7487.PowerLoadAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7487,
        )

        return self.__parent__._cast(_7487.PowerLoadAdvancedSystemDeflection)

    @property
    def pulley_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7488.PulleyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7488,
        )

        return self.__parent__._cast(_7488.PulleyAdvancedSystemDeflection)

    @property
    def ring_pins_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7489.RingPinsAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7489,
        )

        return self.__parent__._cast(_7489.RingPinsAdvancedSystemDeflection)

    @property
    def rolling_ring_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7491.RollingRingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7491,
        )

        return self.__parent__._cast(_7491.RollingRingAdvancedSystemDeflection)

    @property
    def shaft_hub_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7496.ShaftHubConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7496,
        )

        return self.__parent__._cast(_7496.ShaftHubConnectionAdvancedSystemDeflection)

    @property
    def spiral_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7499.SpiralBevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7499,
        )

        return self.__parent__._cast(_7499.SpiralBevelGearAdvancedSystemDeflection)

    @property
    def spring_damper_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7504.SpringDamperHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7504,
        )

        return self.__parent__._cast(_7504.SpringDamperHalfAdvancedSystemDeflection)

    @property
    def straight_bevel_diff_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7505.StraightBevelDiffGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7505,
        )

        return self.__parent__._cast(
            _7505.StraightBevelDiffGearAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7508.StraightBevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7508,
        )

        return self.__parent__._cast(_7508.StraightBevelGearAdvancedSystemDeflection)

    @property
    def straight_bevel_planet_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7511.StraightBevelPlanetGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7511,
        )

        return self.__parent__._cast(
            _7511.StraightBevelPlanetGearAdvancedSystemDeflection
        )

    @property
    def straight_bevel_sun_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7512.StraightBevelSunGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7512,
        )

        return self.__parent__._cast(_7512.StraightBevelSunGearAdvancedSystemDeflection)

    @property
    def synchroniser_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7514.SynchroniserHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7514,
        )

        return self.__parent__._cast(_7514.SynchroniserHalfAdvancedSystemDeflection)

    @property
    def synchroniser_part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7515.SynchroniserPartAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7515,
        )

        return self.__parent__._cast(_7515.SynchroniserPartAdvancedSystemDeflection)

    @property
    def synchroniser_sleeve_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7516.SynchroniserSleeveAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7516,
        )

        return self.__parent__._cast(_7516.SynchroniserSleeveAdvancedSystemDeflection)

    @property
    def torque_converter_pump_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7519.TorqueConverterPumpAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7519,
        )

        return self.__parent__._cast(_7519.TorqueConverterPumpAdvancedSystemDeflection)

    @property
    def torque_converter_turbine_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7520.TorqueConverterTurbineAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7520,
        )

        return self.__parent__._cast(
            _7520.TorqueConverterTurbineAdvancedSystemDeflection
        )

    @property
    def unbalanced_mass_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7522.UnbalancedMassAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7522,
        )

        return self.__parent__._cast(_7522.UnbalancedMassAdvancedSystemDeflection)

    @property
    def virtual_component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7523.VirtualComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7523,
        )

        return self.__parent__._cast(_7523.VirtualComponentAdvancedSystemDeflection)

    @property
    def worm_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7524.WormGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7524,
        )

        return self.__parent__._cast(_7524.WormGearAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7527.ZerolBevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7527,
        )

        return self.__parent__._cast(_7527.ZerolBevelGearAdvancedSystemDeflection)

    @property
    def mountable_component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "MountableComponentAdvancedSystemDeflection":
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
class MountableComponentAdvancedSystemDeflection(
    _7420.ComponentAdvancedSystemDeflection
):
    """MountableComponentAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2693.MountableComponent":
        """mastapy.system_model.part_model.MountableComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponentAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentAdvancedSystemDeflection
        """
        return _Cast_MountableComponentAdvancedSystemDeflection(self)
