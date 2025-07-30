"""RootAssemblyMultibodyDynamicsAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5667

_ROOT_ASSEMBLY_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "RootAssemblyMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7891,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5659,
        _5751,
        _5753,
    )
    from mastapy._private.system_model.part_model import _2706

    Self = TypeVar("Self", bound="RootAssemblyMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RootAssemblyMultibodyDynamicsAnalysis._Cast_RootAssemblyMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RootAssemblyMultibodyDynamicsAnalysis:
    """Special nested class for casting RootAssemblyMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "RootAssemblyMultibodyDynamicsAnalysis"

    @property
    def assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5667.AssemblyMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5667.AssemblyMultibodyDynamicsAnalysis)

    @property
    def abstract_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5659.AbstractAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5659,
        )

        return self.__parent__._cast(_5659.AbstractAssemblyMultibodyDynamicsAnalysis)

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
    def root_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "RootAssemblyMultibodyDynamicsAnalysis":
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
class RootAssemblyMultibodyDynamicsAnalysis(_5667.AssemblyMultibodyDynamicsAnalysis):
    """RootAssemblyMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROOT_ASSEMBLY_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def actual_torque_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActualTorqueRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def actual_torque_ratio_turbine_to_output(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActualTorqueRatioTurbineToOutput")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def brake_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BrakeForce")

        if temp is None:
            return 0.0

        return temp

    @brake_force.setter
    @exception_bridge
    @enforce_parameter_types
    def brake_force(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BrakeForce", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def current_target_vehicle_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentTargetVehicleSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def efficiency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Efficiency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def energy_lost(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnergyLost")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force_from_road_incline(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceFromRoadIncline")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force_from_wheels(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceFromWheels")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def input_energy(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InputEnergy")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def input_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InputPower")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def log_10_time_step(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Log10TimeStep")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def log_10_time_step_requested_by_solver(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Log10TimeStepRequestedBySolver")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_vehicle_speed_error(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumVehicleSpeedError")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def oil_dynamic_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilDynamicTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def overall_efficiency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverallEfficiency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def percentage_error_in_vehicle_speed_compared_to_drive_cycle(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PercentageErrorInVehicleSpeedComparedToDriveCycle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def road_incline(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RoadIncline")

        if temp is None:
            return 0.0

        return temp

    @road_incline.setter
    @exception_bridge
    @enforce_parameter_types
    def road_incline(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RoadIncline", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def total_force_on_vehicle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalForceOnVehicle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def vehicle_acceleration(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VehicleAcceleration")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def vehicle_drag(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VehicleDrag")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def vehicle_position(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VehiclePosition")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def vehicle_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VehicleSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def vehicle_speed_drive_cycle_error(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VehicleSpeedDriveCycleError")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2706.RootAssembly":
        """mastapy.system_model.part_model.RootAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def multibody_dynamics_analysis_inputs(
        self: "Self",
    ) -> "_5751.MultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MultibodyDynamicsAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MultibodyDynamicsAnalysisInputs")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RootAssemblyMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_RootAssemblyMultibodyDynamicsAnalysis
        """
        return _Cast_RootAssemblyMultibodyDynamicsAnalysis(self)
