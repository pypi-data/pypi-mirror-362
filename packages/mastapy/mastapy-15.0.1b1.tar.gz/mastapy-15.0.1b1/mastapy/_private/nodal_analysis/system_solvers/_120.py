"""StepHalvingTransientSolver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.system_solvers import _110

_STEP_HALVING_TRANSIENT_SOLVER = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers", "StepHalvingTransientSolver"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.system_solvers import (
        _106,
        _109,
        _111,
        _112,
        _115,
        _119,
        _121,
        _123,
        _124,
    )

    Self = TypeVar("Self", bound="StepHalvingTransientSolver")
    CastSelf = TypeVar(
        "CastSelf", bound="StepHalvingTransientSolver._Cast_StepHalvingTransientSolver"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StepHalvingTransientSolver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StepHalvingTransientSolver:
    """Special nested class for casting StepHalvingTransientSolver to subclasses."""

    __parent__: "StepHalvingTransientSolver"

    @property
    def internal_transient_solver(self: "CastSelf") -> "_110.InternalTransientSolver":
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
    def wilson_theta_transient_solver(
        self: "CastSelf",
    ) -> "_124.WilsonThetaTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _124

        return self.__parent__._cast(_124.WilsonThetaTransientSolver)

    @property
    def step_halving_transient_solver(self: "CastSelf") -> "StepHalvingTransientSolver":
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
class StepHalvingTransientSolver(_110.InternalTransientSolver):
    """StepHalvingTransientSolver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STEP_HALVING_TRANSIENT_SOLVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_StepHalvingTransientSolver":
        """Cast to another type.

        Returns:
            _Cast_StepHalvingTransientSolver
        """
        return _Cast_StepHalvingTransientSolver(self)
