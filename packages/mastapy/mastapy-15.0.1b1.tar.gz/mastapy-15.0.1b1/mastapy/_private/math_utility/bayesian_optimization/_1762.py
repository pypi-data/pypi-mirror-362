"""BayesianOptimizationVariable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility.optimisation import _1729

_BAYESIAN_OPTIMIZATION_VARIABLE = python_net_import(
    "SMT.MastaAPI.MathUtility.BayesianOptimization", "BayesianOptimizationVariable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BayesianOptimizationVariable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BayesianOptimizationVariable._Cast_BayesianOptimizationVariable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BayesianOptimizationVariable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BayesianOptimizationVariable:
    """Special nested class for casting BayesianOptimizationVariable to subclasses."""

    __parent__: "BayesianOptimizationVariable"

    @property
    def optimization_variable(self: "CastSelf") -> "_1729.OptimizationVariable":
        return self.__parent__._cast(_1729.OptimizationVariable)

    @property
    def bayesian_optimization_variable(
        self: "CastSelf",
    ) -> "BayesianOptimizationVariable":
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
class BayesianOptimizationVariable(_1729.OptimizationVariable):
    """BayesianOptimizationVariable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BAYESIAN_OPTIMIZATION_VARIABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BayesianOptimizationVariable":
        """Cast to another type.

        Returns:
            _Cast_BayesianOptimizationVariable
        """
        return _Cast_BayesianOptimizationVariable(self)
