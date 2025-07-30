"""MountableComponentMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5688

_MOUNTABLE_COMPONENT_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "MountableComponentMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7891,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5664,
        _5669,
        _5674,
        _5676,
        _5677,
        _5679,
        _5684,
        _5690,
        _5693,
        _5696,
        _5699,
        _5701,
        _5705,
        _5711,
        _5713,
        _5717,
        _5723,
        _5727,
        _5735,
        _5738,
        _5741,
        _5743,
        _5747,
        _5752,
        _5753,
        _5755,
        _5759,
        _5760,
        _5761,
        _5762,
        _5763,
        _5767,
        _5771,
        _5777,
        _5781,
        _5784,
        _5787,
        _5789,
        _5790,
        _5791,
        _5793,
        _5794,
        _5798,
        _5800,
        _5801,
        _5802,
        _5805,
        _5808,
    )
    from mastapy._private.system_model.part_model import _2693

    Self = TypeVar("Self", bound="MountableComponentMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentMultibodyDynamicsAnalysis._Cast_MountableComponentMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentMultibodyDynamicsAnalysis:
    """Special nested class for casting MountableComponentMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "MountableComponentMultibodyDynamicsAnalysis"

    @property
    def component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5688.ComponentMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5688.ComponentMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5753.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5753,
        )

        return self.__parent__._cast(_5753.PartMultibodyDynamicsAnalysis)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7891.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7891,
        )

        return self.__parent__._cast(_7891.PartTimeSeriesLoadAnalysisCase)

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
    def agma_gleason_conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5664.AGMAGleasonConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5664,
        )

        return self.__parent__._cast(
            _5664.AGMAGleasonConicalGearMultibodyDynamicsAnalysis
        )

    @property
    def bearing_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5669.BearingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5669,
        )

        return self.__parent__._cast(_5669.BearingMultibodyDynamicsAnalysis)

    @property
    def bevel_differential_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5674.BevelDifferentialGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5674,
        )

        return self.__parent__._cast(
            _5674.BevelDifferentialGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5676.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5676,
        )

        return self.__parent__._cast(
            _5676.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_sun_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5677.BevelDifferentialSunGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5677,
        )

        return self.__parent__._cast(
            _5677.BevelDifferentialSunGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5679.BevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5679,
        )

        return self.__parent__._cast(_5679.BevelGearMultibodyDynamicsAnalysis)

    @property
    def clutch_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5684.ClutchHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5684,
        )

        return self.__parent__._cast(_5684.ClutchHalfMultibodyDynamicsAnalysis)

    @property
    def concept_coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5690.ConceptCouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5690,
        )

        return self.__parent__._cast(_5690.ConceptCouplingHalfMultibodyDynamicsAnalysis)

    @property
    def concept_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5693.ConceptGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5693,
        )

        return self.__parent__._cast(_5693.ConceptGearMultibodyDynamicsAnalysis)

    @property
    def conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5696.ConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5696,
        )

        return self.__parent__._cast(_5696.ConicalGearMultibodyDynamicsAnalysis)

    @property
    def connector_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5699.ConnectorMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5699,
        )

        return self.__parent__._cast(_5699.ConnectorMultibodyDynamicsAnalysis)

    @property
    def coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5701.CouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5701,
        )

        return self.__parent__._cast(_5701.CouplingHalfMultibodyDynamicsAnalysis)

    @property
    def cvt_pulley_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5705.CVTPulleyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5705,
        )

        return self.__parent__._cast(_5705.CVTPulleyMultibodyDynamicsAnalysis)

    @property
    def cylindrical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5711.CylindricalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5711,
        )

        return self.__parent__._cast(_5711.CylindricalGearMultibodyDynamicsAnalysis)

    @property
    def cylindrical_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5713.CylindricalPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5713,
        )

        return self.__parent__._cast(
            _5713.CylindricalPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def face_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5717.FaceGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5717,
        )

        return self.__parent__._cast(_5717.FaceGearMultibodyDynamicsAnalysis)

    @property
    def gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5723.GearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5723,
        )

        return self.__parent__._cast(_5723.GearMultibodyDynamicsAnalysis)

    @property
    def hypoid_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5727.HypoidGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5727,
        )

        return self.__parent__._cast(_5727.HypoidGearMultibodyDynamicsAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5735.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5735,
        )

        return self.__parent__._cast(
            _5735.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5738.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5738,
        )

        return self.__parent__._cast(
            _5738.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5741.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5741,
        )

        return self.__parent__._cast(
            _5741.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis
        )

    @property
    def mass_disc_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5743.MassDiscMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5743,
        )

        return self.__parent__._cast(_5743.MassDiscMultibodyDynamicsAnalysis)

    @property
    def measurement_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5747.MeasurementComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5747,
        )

        return self.__parent__._cast(
            _5747.MeasurementComponentMultibodyDynamicsAnalysis
        )

    @property
    def oil_seal_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5752.OilSealMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5752,
        )

        return self.__parent__._cast(_5752.OilSealMultibodyDynamicsAnalysis)

    @property
    def part_to_part_shear_coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5755.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5755,
        )

        return self.__parent__._cast(
            _5755.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis
        )

    @property
    def planet_carrier_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5759.PlanetCarrierMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5759,
        )

        return self.__parent__._cast(_5759.PlanetCarrierMultibodyDynamicsAnalysis)

    @property
    def point_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5760.PointLoadMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5760,
        )

        return self.__parent__._cast(_5760.PointLoadMultibodyDynamicsAnalysis)

    @property
    def power_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5761.PowerLoadMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5761,
        )

        return self.__parent__._cast(_5761.PowerLoadMultibodyDynamicsAnalysis)

    @property
    def pulley_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5762.PulleyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5762,
        )

        return self.__parent__._cast(_5762.PulleyMultibodyDynamicsAnalysis)

    @property
    def ring_pins_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5763.RingPinsMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5763,
        )

        return self.__parent__._cast(_5763.RingPinsMultibodyDynamicsAnalysis)

    @property
    def rolling_ring_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5767.RollingRingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5767,
        )

        return self.__parent__._cast(_5767.RollingRingMultibodyDynamicsAnalysis)

    @property
    def shaft_hub_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5771.ShaftHubConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5771,
        )

        return self.__parent__._cast(_5771.ShaftHubConnectionMultibodyDynamicsAnalysis)

    @property
    def spiral_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5777.SpiralBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5777,
        )

        return self.__parent__._cast(_5777.SpiralBevelGearMultibodyDynamicsAnalysis)

    @property
    def spring_damper_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5781.SpringDamperHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5781,
        )

        return self.__parent__._cast(_5781.SpringDamperHalfMultibodyDynamicsAnalysis)

    @property
    def straight_bevel_diff_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5784.StraightBevelDiffGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5784,
        )

        return self.__parent__._cast(
            _5784.StraightBevelDiffGearMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5787.StraightBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5787,
        )

        return self.__parent__._cast(_5787.StraightBevelGearMultibodyDynamicsAnalysis)

    @property
    def straight_bevel_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5789.StraightBevelPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5789,
        )

        return self.__parent__._cast(
            _5789.StraightBevelPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_sun_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5790.StraightBevelSunGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5790,
        )

        return self.__parent__._cast(
            _5790.StraightBevelSunGearMultibodyDynamicsAnalysis
        )

    @property
    def synchroniser_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5791.SynchroniserHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5791,
        )

        return self.__parent__._cast(_5791.SynchroniserHalfMultibodyDynamicsAnalysis)

    @property
    def synchroniser_part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5793.SynchroniserPartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5793,
        )

        return self.__parent__._cast(_5793.SynchroniserPartMultibodyDynamicsAnalysis)

    @property
    def synchroniser_sleeve_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5794.SynchroniserSleeveMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5794,
        )

        return self.__parent__._cast(_5794.SynchroniserSleeveMultibodyDynamicsAnalysis)

    @property
    def torque_converter_pump_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5798.TorqueConverterPumpMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5798,
        )

        return self.__parent__._cast(_5798.TorqueConverterPumpMultibodyDynamicsAnalysis)

    @property
    def torque_converter_turbine_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5800.TorqueConverterTurbineMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5800,
        )

        return self.__parent__._cast(
            _5800.TorqueConverterTurbineMultibodyDynamicsAnalysis
        )

    @property
    def unbalanced_mass_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5801.UnbalancedMassMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5801,
        )

        return self.__parent__._cast(_5801.UnbalancedMassMultibodyDynamicsAnalysis)

    @property
    def virtual_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5802.VirtualComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5802,
        )

        return self.__parent__._cast(_5802.VirtualComponentMultibodyDynamicsAnalysis)

    @property
    def worm_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5805.WormGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5805,
        )

        return self.__parent__._cast(_5805.WormGearMultibodyDynamicsAnalysis)

    @property
    def zerol_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5808.ZerolBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5808,
        )

        return self.__parent__._cast(_5808.ZerolBevelGearMultibodyDynamicsAnalysis)

    @property
    def mountable_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "MountableComponentMultibodyDynamicsAnalysis":
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
class MountableComponentMultibodyDynamicsAnalysis(
    _5688.ComponentMultibodyDynamicsAnalysis
):
    """MountableComponentMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def elastic_acceleration_force(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticAccelerationForce")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def elastic_acceleration_moment(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticAccelerationMoment")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def elastic_quadratic_velocity_force(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticQuadraticVelocityForce")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def elastic_quadratic_velocity_moment(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticQuadraticVelocityMoment")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def reference_acceleration_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceAccelerationTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reference_quadratic_velocity_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceQuadraticVelocityTorque")

        if temp is None:
            return 0.0

        return temp

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
    def cast_to(self: "Self") -> "_Cast_MountableComponentMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentMultibodyDynamicsAnalysis
        """
        return _Cast_MountableComponentMultibodyDynamicsAnalysis(self)
