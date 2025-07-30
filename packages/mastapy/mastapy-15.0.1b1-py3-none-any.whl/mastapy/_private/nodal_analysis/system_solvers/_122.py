"""ThermalSolver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.system_solvers import _119

_THERMAL_SOLVER = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers", "ThermalSolver"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ThermalSolver")
    CastSelf = TypeVar("CastSelf", bound="ThermalSolver._Cast_ThermalSolver")


__docformat__ = "restructuredtext en"
__all__ = ("ThermalSolver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalSolver:
    """Special nested class for casting ThermalSolver to subclasses."""

    __parent__: "ThermalSolver"

    @property
    def solver(self: "CastSelf") -> "_119.Solver":
        return self.__parent__._cast(_119.Solver)

    @property
    def thermal_solver(self: "CastSelf") -> "ThermalSolver":
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
class ThermalSolver(_119.Solver):
    """ThermalSolver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_SOLVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ThermalSolver":
        """Cast to another type.

        Returns:
            _Cast_ThermalSolver
        """
        return _Cast_ThermalSolver(self)
