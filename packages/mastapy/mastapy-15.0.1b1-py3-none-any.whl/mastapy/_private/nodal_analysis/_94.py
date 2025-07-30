"""TransientSolverOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis import _74

_TRANSIENT_SOLVER_OPTIONS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "TransientSolverOptions"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.nodal_analysis import _59, _89, _96

    Self = TypeVar("Self", bound="TransientSolverOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="TransientSolverOptions._Cast_TransientSolverOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TransientSolverOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TransientSolverOptions:
    """Special nested class for casting TransientSolverOptions to subclasses."""

    __parent__: "TransientSolverOptions"

    @property
    def transient_solver_options(self: "CastSelf") -> "TransientSolverOptions":
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
class TransientSolverOptions(_0.APIBase):
    """TransientSolverOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TRANSIENT_SOLVER_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def absolute_tolerance_angular_velocity_for_newton_raphson(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AbsoluteToleranceAngularVelocityForNewtonRaphson"
        )

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_angular_velocity_for_newton_raphson.setter
    @exception_bridge
    @enforce_parameter_types
    def absolute_tolerance_angular_velocity_for_newton_raphson(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AbsoluteToleranceAngularVelocityForNewtonRaphson",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def absolute_tolerance_angular_velocity_for_step(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AbsoluteToleranceAngularVelocityForStep"
        )

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_angular_velocity_for_step.setter
    @exception_bridge
    @enforce_parameter_types
    def absolute_tolerance_angular_velocity_for_step(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AbsoluteToleranceAngularVelocityForStep",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def absolute_tolerance_lagrange_force_for_newton_raphson(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AbsoluteToleranceLagrangeForceForNewtonRaphson"
        )

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_lagrange_force_for_newton_raphson.setter
    @exception_bridge
    @enforce_parameter_types
    def absolute_tolerance_lagrange_force_for_newton_raphson(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AbsoluteToleranceLagrangeForceForNewtonRaphson",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def absolute_tolerance_lagrange_moment_for_newton_raphson(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AbsoluteToleranceLagrangeMomentForNewtonRaphson"
        )

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_lagrange_moment_for_newton_raphson.setter
    @exception_bridge
    @enforce_parameter_types
    def absolute_tolerance_lagrange_moment_for_newton_raphson(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AbsoluteToleranceLagrangeMomentForNewtonRaphson",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def absolute_tolerance_simple(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AbsoluteToleranceSimple")

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_simple.setter
    @exception_bridge
    @enforce_parameter_types
    def absolute_tolerance_simple(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AbsoluteToleranceSimple",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def absolute_tolerance_temperature_for_newton_raphson(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AbsoluteToleranceTemperatureForNewtonRaphson"
        )

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_temperature_for_newton_raphson.setter
    @exception_bridge
    @enforce_parameter_types
    def absolute_tolerance_temperature_for_newton_raphson(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AbsoluteToleranceTemperatureForNewtonRaphson",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def absolute_tolerance_temperature_for_step(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AbsoluteToleranceTemperatureForStep"
        )

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_temperature_for_step.setter
    @exception_bridge
    @enforce_parameter_types
    def absolute_tolerance_temperature_for_step(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AbsoluteToleranceTemperatureForStep",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def absolute_tolerance_translational_velocity_for_newton_raphson(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AbsoluteToleranceTranslationalVelocityForNewtonRaphson"
        )

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_translational_velocity_for_newton_raphson.setter
    @exception_bridge
    @enforce_parameter_types
    def absolute_tolerance_translational_velocity_for_newton_raphson(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AbsoluteToleranceTranslationalVelocityForNewtonRaphson",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def absolute_tolerance_translational_velocity_for_step(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AbsoluteToleranceTranslationalVelocityForStep"
        )

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_translational_velocity_for_step.setter
    @exception_bridge
    @enforce_parameter_types
    def absolute_tolerance_translational_velocity_for_step(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AbsoluteToleranceTranslationalVelocityForStep",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def damping_scaling_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DampingScalingFactor")

        if temp is None:
            return 0.0

        return temp

    @damping_scaling_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def damping_scaling_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DampingScalingFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def damping_scaling_for_initial_transients(
        self: "Self",
    ) -> "_59.DampingScalingTypeForInitialTransients":
        """mastapy.nodal_analysis.DampingScalingTypeForInitialTransients"""
        temp = pythonnet_property_get(
            self.wrapped, "DampingScalingForInitialTransients"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.DampingScalingTypeForInitialTransients"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._59",
            "DampingScalingTypeForInitialTransients",
        )(value)

    @damping_scaling_for_initial_transients.setter
    @exception_bridge
    @enforce_parameter_types
    def damping_scaling_for_initial_transients(
        self: "Self", value: "_59.DampingScalingTypeForInitialTransients"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.DampingScalingTypeForInitialTransients"
        )
        pythonnet_property_set(
            self.wrapped, "DampingScalingForInitialTransients", value
        )

    @property
    @exception_bridge
    def end_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EndTime")

        if temp is None:
            return 0.0

        return temp

    @end_time.setter
    @exception_bridge
    @enforce_parameter_types
    def end_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EndTime", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def integration_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_IntegrationMethod":
        """EnumWithSelectedValue[mastapy.nodal_analysis.IntegrationMethod]"""
        temp = pythonnet_property_get(self.wrapped, "IntegrationMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_IntegrationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @integration_method.setter
    @exception_bridge
    @enforce_parameter_types
    def integration_method(self: "Self", value: "_74.IntegrationMethod") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_IntegrationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "IntegrationMethod", value)

    @property
    @exception_bridge
    def limit_time_step_for_final_results(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LimitTimeStepForFinalResults")

        if temp is None:
            return False

        return temp

    @limit_time_step_for_final_results.setter
    @exception_bridge
    @enforce_parameter_types
    def limit_time_step_for_final_results(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LimitTimeStepForFinalResults",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def log_initial_transients(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LogInitialTransients")

        if temp is None:
            return False

        return temp

    @log_initial_transients.setter
    @exception_bridge
    @enforce_parameter_types
    def log_initial_transients(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LogInitialTransients",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def maximum_number_of_time_steps(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfTimeSteps")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @maximum_number_of_time_steps.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_time_steps(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumNumberOfTimeSteps", value)

    @property
    @exception_bridge
    def maximum_time_step(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumTimeStep")

        if temp is None:
            return 0.0

        return temp

    @maximum_time_step.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_time_step(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumTimeStep", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def maximum_time_step_for_final_results(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumTimeStepForFinalResults")

        if temp is None:
            return 0.0

        return temp

    @maximum_time_step_for_final_results.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_time_step_for_final_results(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumTimeStepForFinalResults",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_step_between_results(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumStepBetweenResults")

        if temp is None:
            return 0.0

        return temp

    @minimum_step_between_results.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_step_between_results(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumStepBetweenResults",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_time_step(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumTimeStep")

        if temp is None:
            return 0.0

        return temp

    @minimum_time_step.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_time_step(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MinimumTimeStep", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def rayleigh_damping_alpha(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RayleighDampingAlpha")

        if temp is None:
            return 0.0

        return temp

    @rayleigh_damping_alpha.setter
    @exception_bridge
    @enforce_parameter_types
    def rayleigh_damping_alpha(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RayleighDampingAlpha",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rayleigh_damping_beta(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RayleighDampingBeta")

        if temp is None:
            return 0.0

        return temp

    @rayleigh_damping_beta.setter
    @exception_bridge
    @enforce_parameter_types
    def rayleigh_damping_beta(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RayleighDampingBeta",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relative_tolerance_simple(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RelativeToleranceSimple")

        if temp is None:
            return 0.0

        return temp

    @relative_tolerance_simple.setter
    @exception_bridge
    @enforce_parameter_types
    def relative_tolerance_simple(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RelativeToleranceSimple",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relative_tolerance_for_newton_raphson(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RelativeToleranceForNewtonRaphson")

        if temp is None:
            return 0.0

        return temp

    @relative_tolerance_for_newton_raphson.setter
    @exception_bridge
    @enforce_parameter_types
    def relative_tolerance_for_newton_raphson(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RelativeToleranceForNewtonRaphson",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relative_tolerance_for_step(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RelativeToleranceForStep")

        if temp is None:
            return 0.0

        return temp

    @relative_tolerance_for_step.setter
    @exception_bridge
    @enforce_parameter_types
    def relative_tolerance_for_step(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RelativeToleranceForStep",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def residual_force_tolerance_for_newton_raphson(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ResidualForceToleranceForNewtonRaphson"
        )

        if temp is None:
            return 0.0

        return temp

    @residual_force_tolerance_for_newton_raphson.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_force_tolerance_for_newton_raphson(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ResidualForceToleranceForNewtonRaphson",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def residual_lagrange_angular_tolerance_for_newton_raphson(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ResidualLagrangeAngularToleranceForNewtonRaphson"
        )

        if temp is None:
            return 0.0

        return temp

    @residual_lagrange_angular_tolerance_for_newton_raphson.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_lagrange_angular_tolerance_for_newton_raphson(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ResidualLagrangeAngularToleranceForNewtonRaphson",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def residual_lagrange_translational_tolerance_for_newton_raphson(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ResidualLagrangeTranslationalToleranceForNewtonRaphson"
        )

        if temp is None:
            return 0.0

        return temp

    @residual_lagrange_translational_tolerance_for_newton_raphson.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_lagrange_translational_tolerance_for_newton_raphson(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ResidualLagrangeTranslationalToleranceForNewtonRaphson",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def residual_moment_tolerance_for_newton_raphson(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ResidualMomentToleranceForNewtonRaphson"
        )

        if temp is None:
            return 0.0

        return temp

    @residual_moment_tolerance_for_newton_raphson.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_moment_tolerance_for_newton_raphson(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ResidualMomentToleranceForNewtonRaphson",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def residual_relative_tolerance_for_newton_raphson(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ResidualRelativeToleranceForNewtonRaphson"
        )

        if temp is None:
            return 0.0

        return temp

    @residual_relative_tolerance_for_newton_raphson.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_relative_tolerance_for_newton_raphson(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ResidualRelativeToleranceForNewtonRaphson",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def residual_temperature_tolerance_for_newton_raphson(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ResidualTemperatureToleranceForNewtonRaphson"
        )

        if temp is None:
            return 0.0

        return temp

    @residual_temperature_tolerance_for_newton_raphson.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_temperature_tolerance_for_newton_raphson(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ResidualTemperatureToleranceForNewtonRaphson",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def result_logging_frequency(self: "Self") -> "_89.ResultLoggingFrequency":
        """mastapy.nodal_analysis.ResultLoggingFrequency"""
        temp = pythonnet_property_get(self.wrapped, "ResultLoggingFrequency")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.ResultLoggingFrequency"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._89", "ResultLoggingFrequency"
        )(value)

    @result_logging_frequency.setter
    @exception_bridge
    @enforce_parameter_types
    def result_logging_frequency(
        self: "Self", value: "_89.ResultLoggingFrequency"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.ResultLoggingFrequency"
        )
        pythonnet_property_set(self.wrapped, "ResultLoggingFrequency", value)

    @property
    @exception_bridge
    def rotate_connections_with_bodies(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RotateConnectionsWithBodies")

        if temp is None:
            return False

        return temp

    @rotate_connections_with_bodies.setter
    @exception_bridge
    @enforce_parameter_types
    def rotate_connections_with_bodies(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotateConnectionsWithBodies",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def solver_tolerance_input_method(
        self: "Self",
    ) -> "_96.TransientSolverToleranceInputMethod":
        """mastapy.nodal_analysis.TransientSolverToleranceInputMethod"""
        temp = pythonnet_property_get(self.wrapped, "SolverToleranceInputMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.TransientSolverToleranceInputMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._96", "TransientSolverToleranceInputMethod"
        )(value)

    @solver_tolerance_input_method.setter
    @exception_bridge
    @enforce_parameter_types
    def solver_tolerance_input_method(
        self: "Self", value: "_96.TransientSolverToleranceInputMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.TransientSolverToleranceInputMethod"
        )
        pythonnet_property_set(self.wrapped, "SolverToleranceInputMethod", value)

    @property
    @exception_bridge
    def theta(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Theta")

        if temp is None:
            return 0.0

        return temp

    @theta.setter
    @exception_bridge
    @enforce_parameter_types
    def theta(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Theta", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def time_for_initial_transients(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TimeForInitialTransients")

        if temp is None:
            return 0.0

        return temp

    @time_for_initial_transients.setter
    @exception_bridge
    @enforce_parameter_types
    def time_for_initial_transients(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TimeForInitialTransients",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def time_step_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TimeStepLength")

        if temp is None:
            return 0.0

        return temp

    @time_step_length.setter
    @exception_bridge
    @enforce_parameter_types
    def time_step_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TimeStepLength", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def time_to_start_using_final_results_maximum_time_step(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TimeToStartUsingFinalResultsMaximumTimeStep"
        )

        if temp is None:
            return 0.0

        return temp

    @time_to_start_using_final_results_maximum_time_step.setter
    @exception_bridge
    @enforce_parameter_types
    def time_to_start_using_final_results_maximum_time_step(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "TimeToStartUsingFinalResultsMaximumTimeStep",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TransientSolverOptions":
        """Cast to another type.

        Returns:
            _Cast_TransientSolverOptions
        """
        return _Cast_TransientSolverOptions(self)
