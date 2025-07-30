"""ML1OptimiserSnapshot"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_ML1_OPTIMISER_SNAPSHOT = python_net_import(
    "SMT.MastaAPI.MathUtility.BayesianOptimization", "ML1OptimiserSnapshot"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility.bayesian_optimization import _1763, _1764, _1769

    Self = TypeVar("Self", bound="ML1OptimiserSnapshot")
    CastSelf = TypeVar(
        "CastSelf", bound="ML1OptimiserSnapshot._Cast_ML1OptimiserSnapshot"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ML1OptimiserSnapshot",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ML1OptimiserSnapshot:
    """Special nested class for casting ML1OptimiserSnapshot to subclasses."""

    __parent__: "ML1OptimiserSnapshot"

    @property
    def ml1_optimiser_snapshot(self: "CastSelf") -> "ML1OptimiserSnapshot":
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
class ML1OptimiserSnapshot(_0.APIBase):
    """ML1OptimiserSnapshot

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ML1_OPTIMISER_SNAPSHOT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def constraints_met(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConstraintsMet")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def denormalized_objective_function_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DenormalizedObjectiveFunctionValue"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iteration(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Iteration")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def optimization_stage(self: "Self") -> "_1769.OptimizationStage":
        """mastapy.math_utility.bayesian_optimization.OptimizationStage

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OptimizationStage")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.MathUtility.BayesianOptimization.OptimizationStage"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility.bayesian_optimization._1769",
            "OptimizationStage",
        )(value)

    @property
    @exception_bridge
    def constraint_values(self: "Self") -> "List[_1763.ConstraintResult]":
        """List[mastapy.math_utility.bayesian_optimization.ConstraintResult]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConstraintValues")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def input_values(self: "Self") -> "List[_1764.InputResult]":
        """List[mastapy.math_utility.bayesian_optimization.InputResult]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InputValues")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ML1OptimiserSnapshot":
        """Cast to another type.

        Returns:
            _Cast_ML1OptimiserSnapshot
        """
        return _Cast_ML1OptimiserSnapshot(self)
