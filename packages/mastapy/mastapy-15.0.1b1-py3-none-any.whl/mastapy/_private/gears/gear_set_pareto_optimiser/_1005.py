"""BarForPareto"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private.math_utility.optimisation import _1734

_BAR_FOR_PARETO = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "BarForPareto"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.analysis import _1337

    Self = TypeVar("Self", bound="BarForPareto")
    CastSelf = TypeVar("CastSelf", bound="BarForPareto._Cast_BarForPareto")

TAnalysis = TypeVar("TAnalysis", bound="_1337.AbstractGearSetAnalysis")
TCandidate = TypeVar("TCandidate")

__docformat__ = "restructuredtext en"
__all__ = ("BarForPareto",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BarForPareto:
    """Special nested class for casting BarForPareto to subclasses."""

    __parent__: "BarForPareto"

    @property
    def pareto_optimisation_strategy_bars(
        self: "CastSelf",
    ) -> "_1734.ParetoOptimisationStrategyBars":
        return self.__parent__._cast(_1734.ParetoOptimisationStrategyBars)

    @property
    def bar_for_pareto(self: "CastSelf") -> "BarForPareto":
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
class BarForPareto(
    _1734.ParetoOptimisationStrategyBars, Generic[TAnalysis, TCandidate]
):
    """BarForPareto

    This is a mastapy class.

    Generic Types:
        TAnalysis
        TCandidate
    """

    TYPE: ClassVar["Type"] = _BAR_FOR_PARETO

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    def remove_bar(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveBar")

    @property
    def cast_to(self: "Self") -> "_Cast_BarForPareto":
        """Cast to another type.

        Returns:
            _Cast_BarForPareto
        """
        return _Cast_BarForPareto(self)
