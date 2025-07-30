"""ConicalGearOptimizationStep"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.optimization import _2445

_CONICAL_GEAR_OPTIMIZATION_STEP = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization", "ConicalGearOptimizationStep"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalGearOptimizationStep")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearOptimizationStep._Cast_ConicalGearOptimizationStep",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearOptimizationStep",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearOptimizationStep:
    """Special nested class for casting ConicalGearOptimizationStep to subclasses."""

    __parent__: "ConicalGearOptimizationStep"

    @property
    def optimization_step(self: "CastSelf") -> "_2445.OptimizationStep":
        return self.__parent__._cast(_2445.OptimizationStep)

    @property
    def conical_gear_optimization_step(
        self: "CastSelf",
    ) -> "ConicalGearOptimizationStep":
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
class ConicalGearOptimizationStep(_2445.OptimizationStep):
    """ConicalGearOptimizationStep

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_OPTIMIZATION_STEP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearOptimizationStep":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearOptimizationStep
        """
        return _Cast_ConicalGearOptimizationStep(self)
