"""FastPowerFlowSolution"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_FAST_POWER_FLOW_SOLUTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "FastPowerFlowSolution"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FastPowerFlowSolution")
    CastSelf = TypeVar(
        "CastSelf", bound="FastPowerFlowSolution._Cast_FastPowerFlowSolution"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FastPowerFlowSolution",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FastPowerFlowSolution:
    """Special nested class for casting FastPowerFlowSolution to subclasses."""

    __parent__: "FastPowerFlowSolution"

    @property
    def fast_power_flow_solution(self: "CastSelf") -> "FastPowerFlowSolution":
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
class FastPowerFlowSolution(_0.APIBase):
    """FastPowerFlowSolution

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FAST_POWER_FLOW_SOLUTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FastPowerFlowSolution":
        """Cast to another type.

        Returns:
            _Cast_FastPowerFlowSolution
        """
        return _Cast_FastPowerFlowSolution(self)
