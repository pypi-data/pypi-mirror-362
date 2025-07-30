"""SimpleVelocityBasedStepHalvingTransientSolver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.system_solvers import _120

_SIMPLE_VELOCITY_BASED_STEP_HALVING_TRANSIENT_SOLVER = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers",
    "SimpleVelocityBasedStepHalvingTransientSolver",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.system_solvers import (
        _106,
        _109,
        _110,
        _112,
        _119,
        _121,
        _123,
    )

    Self = TypeVar("Self", bound="SimpleVelocityBasedStepHalvingTransientSolver")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SimpleVelocityBasedStepHalvingTransientSolver._Cast_SimpleVelocityBasedStepHalvingTransientSolver",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SimpleVelocityBasedStepHalvingTransientSolver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SimpleVelocityBasedStepHalvingTransientSolver:
    """Special nested class for casting SimpleVelocityBasedStepHalvingTransientSolver to subclasses."""

    __parent__: "SimpleVelocityBasedStepHalvingTransientSolver"

    @property
    def step_halving_transient_solver(
        self: "CastSelf",
    ) -> "_120.StepHalvingTransientSolver":
        return self.__parent__._cast(_120.StepHalvingTransientSolver)

    @property
    def internal_transient_solver(self: "CastSelf") -> "_110.InternalTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _110

        return self.__parent__._cast(_110.InternalTransientSolver)

    @property
    def transient_solver(self: "CastSelf") -> "_123.TransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _123

        return self.__parent__._cast(_123.TransientSolver)

    @property
    def dynamic_solver(self: "CastSelf") -> "_109.DynamicSolver":
        from mastapy._private.nodal_analysis.system_solvers import _109

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
    def newmark_transient_solver(self: "CastSelf") -> "_112.NewmarkTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _112

        return self.__parent__._cast(_112.NewmarkTransientSolver)

    @property
    def simple_velocity_based_step_halving_transient_solver(
        self: "CastSelf",
    ) -> "SimpleVelocityBasedStepHalvingTransientSolver":
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
class SimpleVelocityBasedStepHalvingTransientSolver(_120.StepHalvingTransientSolver):
    """SimpleVelocityBasedStepHalvingTransientSolver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SIMPLE_VELOCITY_BASED_STEP_HALVING_TRANSIENT_SOLVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SimpleVelocityBasedStepHalvingTransientSolver":
        """Cast to another type.

        Returns:
            _Cast_SimpleVelocityBasedStepHalvingTransientSolver
        """
        return _Cast_SimpleVelocityBasedStepHalvingTransientSolver(self)
