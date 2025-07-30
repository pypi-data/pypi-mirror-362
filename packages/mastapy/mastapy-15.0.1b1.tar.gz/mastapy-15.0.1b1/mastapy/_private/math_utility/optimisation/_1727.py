"""OptimizationInput"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility.optimisation import _1729

_OPTIMIZATION_INPUT = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation", "OptimizationInput"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.optimisation import _1740

    Self = TypeVar("Self", bound="OptimizationInput")
    CastSelf = TypeVar("CastSelf", bound="OptimizationInput._Cast_OptimizationInput")


__docformat__ = "restructuredtext en"
__all__ = ("OptimizationInput",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OptimizationInput:
    """Special nested class for casting OptimizationInput to subclasses."""

    __parent__: "OptimizationInput"

    @property
    def optimization_variable(self: "CastSelf") -> "_1729.OptimizationVariable":
        return self.__parent__._cast(_1729.OptimizationVariable)

    @property
    def reporting_optimization_input(
        self: "CastSelf",
    ) -> "_1740.ReportingOptimizationInput":
        from mastapy._private.math_utility.optimisation import _1740

        return self.__parent__._cast(_1740.ReportingOptimizationInput)

    @property
    def optimization_input(self: "CastSelf") -> "OptimizationInput":
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
class OptimizationInput(_1729.OptimizationVariable):
    """OptimizationInput

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OPTIMIZATION_INPUT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_OptimizationInput":
        """Cast to another type.

        Returns:
            _Cast_OptimizationInput
        """
        return _Cast_OptimizationInput(self)
