"""PowerLoadMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5802

_POWER_LOAD_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "PowerLoadMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7891,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5688,
        _5750,
        _5753,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7810
    from mastapy._private.system_model.part_model import _2703

    Self = TypeVar("Self", bound="PowerLoadMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PowerLoadMultibodyDynamicsAnalysis._Cast_PowerLoadMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoadMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PowerLoadMultibodyDynamicsAnalysis:
    """Special nested class for casting PowerLoadMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "PowerLoadMultibodyDynamicsAnalysis"

    @property
    def virtual_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5802.VirtualComponentMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5802.VirtualComponentMultibodyDynamicsAnalysis)

    @property
    def mountable_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5750.MountableComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5750,
        )

        return self.__parent__._cast(_5750.MountableComponentMultibodyDynamicsAnalysis)

    @property
    def component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5688.ComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5688,
        )

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
    def power_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "PowerLoadMultibodyDynamicsAnalysis":
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
class PowerLoadMultibodyDynamicsAnalysis(
    _5802.VirtualComponentMultibodyDynamicsAnalysis
):
    """PowerLoadMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POWER_LOAD_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_jerk_rate_of_change_of_acceleration(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngularJerkRateOfChangeOfAcceleration"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def applied_torque(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AppliedTorque")

        if temp is None:
            return 0.0

        return temp

    @applied_torque.setter
    @exception_bridge
    @enforce_parameter_types
    def applied_torque(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AppliedTorque", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def controller_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ControllerTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def current_coefficient_of_friction_with_ground(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CurrentCoefficientOfFrictionWithGround"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def drag_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DragTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elastic_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def energy_input(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnergyInput")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def engine_idle_speed_control_enabled(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EngineIdleSpeedControlEnabled")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def engine_throttle_from_interface(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EngineThrottleFromInterface")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def engine_throttle_position_over_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EngineThrottlePositionOverTime")

        if temp is None:
            return 0.0

        return temp

    @engine_throttle_position_over_time.setter
    @exception_bridge
    @enforce_parameter_types
    def engine_throttle_position_over_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EngineThrottlePositionOverTime",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def error_in_engine_idle_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ErrorInEngineIdleSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def error_in_target_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ErrorInTargetSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def filtered_engine_throttle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FilteredEngineThrottle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fuel_consumption_instantaneous(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FuelConsumptionInstantaneous")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def interface_input_torque_used_in_solver(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InterfaceInputTorqueUsedInSolver")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def is_locked(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsLocked")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_wheel_using_static_friction(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsWheelUsingStaticFriction")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def lagged_angular_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LaggedAngularVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def longitudinal_slip_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LongitudinalSlipRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_time_step(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumTimeStep")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Power")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_from_vehicle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueFromVehicle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_on_each_wheel(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueOnEachWheel")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_fuel_consumed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalFuelConsumed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def unfiltered_controller_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UnfilteredControllerTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2703.PowerLoad":
        """mastapy.system_model.part_model.PowerLoad

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
    def component_load_case(self: "Self") -> "_7810.PowerLoadLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PowerLoadMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PowerLoadMultibodyDynamicsAnalysis
        """
        return _Cast_PowerLoadMultibodyDynamicsAnalysis(self)
