"""Solver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_SOLVER = python_net_import("SMT.MastaAPI.NodalAnalysis.SystemSolvers", "Solver")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.system_solvers import (
        _106,
        _107,
        _108,
        _109,
        _110,
        _111,
        _112,
        _115,
        _120,
        _121,
        _122,
        _123,
        _124,
    )

    Self = TypeVar("Self", bound="Solver")
    CastSelf = TypeVar("CastSelf", bound="Solver._Cast_Solver")


__docformat__ = "restructuredtext en"
__all__ = ("Solver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Solver:
    """Special nested class for casting Solver to subclasses."""

    __parent__: "Solver"

    @property
    def backward_euler_transient_solver(
        self: "CastSelf",
    ) -> "_106.BackwardEulerTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _106

        return self.__parent__._cast(_106.BackwardEulerTransientSolver)

    @property
    def dense_stiffness_solver(self: "CastSelf") -> "_107.DenseStiffnessSolver":
        from mastapy._private.nodal_analysis.system_solvers import _107

        return self.__parent__._cast(_107.DenseStiffnessSolver)

    @property
    def dirk_transient_solver(self: "CastSelf") -> "_108.DirkTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _108

        return self.__parent__._cast(_108.DirkTransientSolver)

    @property
    def dynamic_solver(self: "CastSelf") -> "_109.DynamicSolver":
        from mastapy._private.nodal_analysis.system_solvers import _109

        return self.__parent__._cast(_109.DynamicSolver)

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
    def stiffness_solver(self: "CastSelf") -> "_121.StiffnessSolver":
        from mastapy._private.nodal_analysis.system_solvers import _121

        return self.__parent__._cast(_121.StiffnessSolver)

    @property
    def thermal_solver(self: "CastSelf") -> "_122.ThermalSolver":
        from mastapy._private.nodal_analysis.system_solvers import _122

        return self.__parent__._cast(_122.ThermalSolver)

    @property
    def transient_solver(self: "CastSelf") -> "_123.TransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _123

        return self.__parent__._cast(_123.TransientSolver)

    @property
    def wilson_theta_transient_solver(
        self: "CastSelf",
    ) -> "_124.WilsonThetaTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _124

        return self.__parent__._cast(_124.WilsonThetaTransientSolver)

    @property
    def solver(self: "CastSelf") -> "Solver":
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
class Solver(_0.APIBase):
    """Solver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SOLVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def average_number_of_jacobian_evaluations_per_newton_raphson_solve(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AverageNumberOfJacobianEvaluationsPerNewtonRaphsonSolve"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_failed_newton_raphson_solves(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfFailedNewtonRaphsonSolves")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_newton_raphson_jacobian_evaluations(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfNewtonRaphsonJacobianEvaluations"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_newton_raphson_maximum_iterations_reached(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfNewtonRaphsonMaximumIterationsReached"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_newton_raphson_other_status_results(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfNewtonRaphsonOtherStatusResults"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_newton_raphson_residual_evaluations(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfNewtonRaphsonResidualEvaluations"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_newton_raphson_residual_tolerance_met(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfNewtonRaphsonResidualToleranceMet"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_newton_raphson_solves(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfNewtonRaphsonSolves")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_newton_raphson_values_not_changing(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfNewtonRaphsonValuesNotChanging"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_nodes(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfNodes")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def total_number_of_degrees_of_freedom(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalNumberOfDegreesOfFreedom")

        if temp is None:
            return 0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_Solver":
        """Cast to another type.

        Returns:
            _Cast_Solver
        """
        return _Cast_Solver(self)
