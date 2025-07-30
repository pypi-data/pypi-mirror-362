"""TransientSolver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.system_solvers import _109

_TRANSIENT_SOLVER = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers", "TransientSolver"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis import _95
    from mastapy._private.nodal_analysis.system_solvers import (
        _106,
        _108,
        _110,
        _111,
        _112,
        _115,
        _119,
        _120,
        _121,
        _124,
    )

    Self = TypeVar("Self", bound="TransientSolver")
    CastSelf = TypeVar("CastSelf", bound="TransientSolver._Cast_TransientSolver")


__docformat__ = "restructuredtext en"
__all__ = ("TransientSolver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TransientSolver:
    """Special nested class for casting TransientSolver to subclasses."""

    __parent__: "TransientSolver"

    @property
    def dynamic_solver(self: "CastSelf") -> "_109.DynamicSolver":
        return self.__parent__._cast(_109.DynamicSolver)

    @property
    def stiffness_solver(self: "CastSelf") -> "_121.StiffnessSolver":
        from mastapy._private.nodal_analysis.system_solvers import _121

        return self.__parent__._cast(_121.StiffnessSolver)

    @property
    def solver(self: "CastSelf") -> "_119.Solver":
        from mastapy._private.nodal_analysis.system_solvers import _119

        return self.__parent__._cast(_119.Solver)

    @property
    def backward_euler_transient_solver(
        self: "CastSelf",
    ) -> "_106.BackwardEulerTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _106

        return self.__parent__._cast(_106.BackwardEulerTransientSolver)

    @property
    def dirk_transient_solver(self: "CastSelf") -> "_108.DirkTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _108

        return self.__parent__._cast(_108.DirkTransientSolver)

    @property
    def internal_transient_solver(self: "CastSelf") -> "_110.InternalTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _110

        return self.__parent__._cast(_110.InternalTransientSolver)

    @property
    def lobatto_iiic_transient_solver(
        self: "CastSelf",
    ) -> "_111.LobattoIIICTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _111

        return self.__parent__._cast(_111.LobattoIIICTransientSolver)

    @property
    def newmark_transient_solver(self: "CastSelf") -> "_112.NewmarkTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _112

        return self.__parent__._cast(_112.NewmarkTransientSolver)

    @property
    def simple_velocity_based_step_halving_transient_solver(
        self: "CastSelf",
    ) -> "_115.SimpleVelocityBasedStepHalvingTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _115

        return self.__parent__._cast(_115.SimpleVelocityBasedStepHalvingTransientSolver)

    @property
    def step_halving_transient_solver(
        self: "CastSelf",
    ) -> "_120.StepHalvingTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _120

        return self.__parent__._cast(_120.StepHalvingTransientSolver)

    @property
    def wilson_theta_transient_solver(
        self: "CastSelf",
    ) -> "_124.WilsonThetaTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _124

        return self.__parent__._cast(_124.WilsonThetaTransientSolver)

    @property
    def transient_solver(self: "CastSelf") -> "TransientSolver":
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
class TransientSolver(_109.DynamicSolver):
    """TransientSolver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TRANSIENT_SOLVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def interface_analysis_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InterfaceAnalysisTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_attempted_single_steps(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfAttemptedSingleSteps")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_failed_time_steps(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfFailedTimeSteps")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_failed_time_steps_at_minimum_time_step(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfFailedTimeStepsAtMinimumTimeStep"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_interface_time_steps(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfInterfaceTimeSteps")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_successful_single_steps(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfSuccessfulSingleSteps")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_time_steps_taken(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfTimeStepsTaken")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_times_single_step_function_failed(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfTimesSingleStepFunctionFailed"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_times_step_error_tolerance_not_met(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfTimesStepErrorToleranceNotMet"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def solver_status(self: "Self") -> "_95.TransientSolverStatus":
        """mastapy.nodal_analysis.TransientSolverStatus"""
        temp = pythonnet_property_get(self.wrapped, "SolverStatus")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.TransientSolverStatus"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._95", "TransientSolverStatus"
        )(value)

    @solver_status.setter
    @exception_bridge
    @enforce_parameter_types
    def solver_status(self: "Self", value: "_95.TransientSolverStatus") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.TransientSolverStatus"
        )
        pythonnet_property_set(self.wrapped, "SolverStatus", value)

    @exception_bridge
    def times_of_logged_results(self: "Self") -> "List[float]":
        """List[float]"""
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "TimesOfLoggedResults"), float
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TransientSolver":
        """Cast to another type.

        Returns:
            _Cast_TransientSolver
        """
        return _Cast_TransientSolver(self)
