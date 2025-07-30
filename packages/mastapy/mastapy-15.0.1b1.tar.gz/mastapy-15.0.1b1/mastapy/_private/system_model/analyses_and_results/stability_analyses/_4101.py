"""MountableComponentStabilityAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.stability_analyses import _4045

_MOUNTABLE_COMPONENT_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "MountableComponentStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4026,
        _4028,
        _4033,
        _4034,
        _4035,
        _4038,
        _4042,
        _4047,
        _4051,
        _4054,
        _4056,
        _4058,
        _4062,
        _4070,
        _4071,
        _4077,
        _4082,
        _4086,
        _4090,
        _4093,
        _4096,
        _4097,
        _4098,
        _4102,
        _4103,
        _4105,
        _4109,
        _4110,
        _4111,
        _4112,
        _4113,
        _4117,
        _4119,
        _4125,
        _4127,
        _4134,
        _4137,
        _4138,
        _4139,
        _4140,
        _4141,
        _4142,
        _4145,
        _4147,
        _4148,
        _4149,
        _4152,
        _4155,
    )
    from mastapy._private.system_model.part_model import _2693

    Self = TypeVar("Self", bound="MountableComponentStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentStabilityAnalysis._Cast_MountableComponentStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentStabilityAnalysis:
    """Special nested class for casting MountableComponentStabilityAnalysis to subclasses."""

    __parent__: "MountableComponentStabilityAnalysis"

    @property
    def component_stability_analysis(
        self: "CastSelf",
    ) -> "_4045.ComponentStabilityAnalysis":
        return self.__parent__._cast(_4045.ComponentStabilityAnalysis)

    @property
    def part_stability_analysis(self: "CastSelf") -> "_4103.PartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4103,
        )

        return self.__parent__._cast(_4103.PartStabilityAnalysis)

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
    def agma_gleason_conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4026.AGMAGleasonConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4026,
        )

        return self.__parent__._cast(_4026.AGMAGleasonConicalGearStabilityAnalysis)

    @property
    def bearing_stability_analysis(
        self: "CastSelf",
    ) -> "_4028.BearingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4028,
        )

        return self.__parent__._cast(_4028.BearingStabilityAnalysis)

    @property
    def bevel_differential_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4033.BevelDifferentialGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4033,
        )

        return self.__parent__._cast(_4033.BevelDifferentialGearStabilityAnalysis)

    @property
    def bevel_differential_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4034.BevelDifferentialPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4034,
        )

        return self.__parent__._cast(_4034.BevelDifferentialPlanetGearStabilityAnalysis)

    @property
    def bevel_differential_sun_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4035.BevelDifferentialSunGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4035,
        )

        return self.__parent__._cast(_4035.BevelDifferentialSunGearStabilityAnalysis)

    @property
    def bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4038.BevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4038,
        )

        return self.__parent__._cast(_4038.BevelGearStabilityAnalysis)

    @property
    def clutch_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4042.ClutchHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4042,
        )

        return self.__parent__._cast(_4042.ClutchHalfStabilityAnalysis)

    @property
    def concept_coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4047.ConceptCouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4047,
        )

        return self.__parent__._cast(_4047.ConceptCouplingHalfStabilityAnalysis)

    @property
    def concept_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4051.ConceptGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4051,
        )

        return self.__parent__._cast(_4051.ConceptGearStabilityAnalysis)

    @property
    def conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4054.ConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4054,
        )

        return self.__parent__._cast(_4054.ConicalGearStabilityAnalysis)

    @property
    def connector_stability_analysis(
        self: "CastSelf",
    ) -> "_4056.ConnectorStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4056,
        )

        return self.__parent__._cast(_4056.ConnectorStabilityAnalysis)

    @property
    def coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4058.CouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4058,
        )

        return self.__parent__._cast(_4058.CouplingHalfStabilityAnalysis)

    @property
    def cvt_pulley_stability_analysis(
        self: "CastSelf",
    ) -> "_4062.CVTPulleyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4062,
        )

        return self.__parent__._cast(_4062.CVTPulleyStabilityAnalysis)

    @property
    def cylindrical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4070.CylindricalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4070,
        )

        return self.__parent__._cast(_4070.CylindricalGearStabilityAnalysis)

    @property
    def cylindrical_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4071.CylindricalPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4071,
        )

        return self.__parent__._cast(_4071.CylindricalPlanetGearStabilityAnalysis)

    @property
    def face_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4077.FaceGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4077,
        )

        return self.__parent__._cast(_4077.FaceGearStabilityAnalysis)

    @property
    def gear_stability_analysis(self: "CastSelf") -> "_4082.GearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4082,
        )

        return self.__parent__._cast(_4082.GearStabilityAnalysis)

    @property
    def hypoid_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4086.HypoidGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4086,
        )

        return self.__parent__._cast(_4086.HypoidGearStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4090.KlingelnbergCycloPalloidConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4090,
        )

        return self.__parent__._cast(
            _4090.KlingelnbergCycloPalloidConicalGearStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4093.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4093,
        )

        return self.__parent__._cast(
            _4093.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4096.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4096,
        )

        return self.__parent__._cast(
            _4096.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis
        )

    @property
    def mass_disc_stability_analysis(
        self: "CastSelf",
    ) -> "_4097.MassDiscStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4097,
        )

        return self.__parent__._cast(_4097.MassDiscStabilityAnalysis)

    @property
    def measurement_component_stability_analysis(
        self: "CastSelf",
    ) -> "_4098.MeasurementComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4098,
        )

        return self.__parent__._cast(_4098.MeasurementComponentStabilityAnalysis)

    @property
    def oil_seal_stability_analysis(
        self: "CastSelf",
    ) -> "_4102.OilSealStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4102,
        )

        return self.__parent__._cast(_4102.OilSealStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4105.PartToPartShearCouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4105,
        )

        return self.__parent__._cast(_4105.PartToPartShearCouplingHalfStabilityAnalysis)

    @property
    def planet_carrier_stability_analysis(
        self: "CastSelf",
    ) -> "_4109.PlanetCarrierStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4109,
        )

        return self.__parent__._cast(_4109.PlanetCarrierStabilityAnalysis)

    @property
    def point_load_stability_analysis(
        self: "CastSelf",
    ) -> "_4110.PointLoadStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4110,
        )

        return self.__parent__._cast(_4110.PointLoadStabilityAnalysis)

    @property
    def power_load_stability_analysis(
        self: "CastSelf",
    ) -> "_4111.PowerLoadStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4111,
        )

        return self.__parent__._cast(_4111.PowerLoadStabilityAnalysis)

    @property
    def pulley_stability_analysis(self: "CastSelf") -> "_4112.PulleyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4112,
        )

        return self.__parent__._cast(_4112.PulleyStabilityAnalysis)

    @property
    def ring_pins_stability_analysis(
        self: "CastSelf",
    ) -> "_4113.RingPinsStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4113,
        )

        return self.__parent__._cast(_4113.RingPinsStabilityAnalysis)

    @property
    def rolling_ring_stability_analysis(
        self: "CastSelf",
    ) -> "_4117.RollingRingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4117,
        )

        return self.__parent__._cast(_4117.RollingRingStabilityAnalysis)

    @property
    def shaft_hub_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4119.ShaftHubConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4119,
        )

        return self.__parent__._cast(_4119.ShaftHubConnectionStabilityAnalysis)

    @property
    def spiral_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4125.SpiralBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4125,
        )

        return self.__parent__._cast(_4125.SpiralBevelGearStabilityAnalysis)

    @property
    def spring_damper_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4127.SpringDamperHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4127,
        )

        return self.__parent__._cast(_4127.SpringDamperHalfStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4134.StraightBevelDiffGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4134,
        )

        return self.__parent__._cast(_4134.StraightBevelDiffGearStabilityAnalysis)

    @property
    def straight_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4137.StraightBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4137,
        )

        return self.__parent__._cast(_4137.StraightBevelGearStabilityAnalysis)

    @property
    def straight_bevel_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4138.StraightBevelPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4138,
        )

        return self.__parent__._cast(_4138.StraightBevelPlanetGearStabilityAnalysis)

    @property
    def straight_bevel_sun_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4139.StraightBevelSunGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4139,
        )

        return self.__parent__._cast(_4139.StraightBevelSunGearStabilityAnalysis)

    @property
    def synchroniser_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4140.SynchroniserHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4140,
        )

        return self.__parent__._cast(_4140.SynchroniserHalfStabilityAnalysis)

    @property
    def synchroniser_part_stability_analysis(
        self: "CastSelf",
    ) -> "_4141.SynchroniserPartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4141,
        )

        return self.__parent__._cast(_4141.SynchroniserPartStabilityAnalysis)

    @property
    def synchroniser_sleeve_stability_analysis(
        self: "CastSelf",
    ) -> "_4142.SynchroniserSleeveStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4142,
        )

        return self.__parent__._cast(_4142.SynchroniserSleeveStabilityAnalysis)

    @property
    def torque_converter_pump_stability_analysis(
        self: "CastSelf",
    ) -> "_4145.TorqueConverterPumpStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4145,
        )

        return self.__parent__._cast(_4145.TorqueConverterPumpStabilityAnalysis)

    @property
    def torque_converter_turbine_stability_analysis(
        self: "CastSelf",
    ) -> "_4147.TorqueConverterTurbineStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4147,
        )

        return self.__parent__._cast(_4147.TorqueConverterTurbineStabilityAnalysis)

    @property
    def unbalanced_mass_stability_analysis(
        self: "CastSelf",
    ) -> "_4148.UnbalancedMassStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4148,
        )

        return self.__parent__._cast(_4148.UnbalancedMassStabilityAnalysis)

    @property
    def virtual_component_stability_analysis(
        self: "CastSelf",
    ) -> "_4149.VirtualComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4149,
        )

        return self.__parent__._cast(_4149.VirtualComponentStabilityAnalysis)

    @property
    def worm_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4152.WormGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4152,
        )

        return self.__parent__._cast(_4152.WormGearStabilityAnalysis)

    @property
    def zerol_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4155.ZerolBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4155,
        )

        return self.__parent__._cast(_4155.ZerolBevelGearStabilityAnalysis)

    @property
    def mountable_component_stability_analysis(
        self: "CastSelf",
    ) -> "MountableComponentStabilityAnalysis":
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
class MountableComponentStabilityAnalysis(_4045.ComponentStabilityAnalysis):
    """MountableComponentStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_STABILITY_ANALYSIS

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
    def cast_to(self: "Self") -> "_Cast_MountableComponentStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentStabilityAnalysis
        """
        return _Cast_MountableComponentStabilityAnalysis(self)
