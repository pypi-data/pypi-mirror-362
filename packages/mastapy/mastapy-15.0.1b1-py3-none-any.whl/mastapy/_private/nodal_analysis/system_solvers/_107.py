"""DenseStiffnessSolver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.system_solvers import _119

_DENSE_STIFFNESS_SOLVER = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers", "DenseStiffnessSolver"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DenseStiffnessSolver")
    CastSelf = TypeVar(
        "CastSelf", bound="DenseStiffnessSolver._Cast_DenseStiffnessSolver"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DenseStiffnessSolver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DenseStiffnessSolver:
    """Special nested class for casting DenseStiffnessSolver to subclasses."""

    __parent__: "DenseStiffnessSolver"

    @property
    def solver(self: "CastSelf") -> "_119.Solver":
        return self.__parent__._cast(_119.Solver)

    @property
    def dense_stiffness_solver(self: "CastSelf") -> "DenseStiffnessSolver":
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
class DenseStiffnessSolver(_119.Solver):
    """DenseStiffnessSolver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DENSE_STIFFNESS_SOLVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DenseStiffnessSolver":
        """Cast to another type.

        Returns:
            _Cast_DenseStiffnessSolver
        """
        return _Cast_DenseStiffnessSolver(self)
