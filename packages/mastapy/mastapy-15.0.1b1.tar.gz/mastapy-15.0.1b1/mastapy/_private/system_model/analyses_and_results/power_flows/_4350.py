"""FastPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_FAST_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "FastPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FastPowerFlow")
    CastSelf = TypeVar("CastSelf", bound="FastPowerFlow._Cast_FastPowerFlow")


__docformat__ = "restructuredtext en"
__all__ = ("FastPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FastPowerFlow:
    """Special nested class for casting FastPowerFlow to subclasses."""

    __parent__: "FastPowerFlow"

    @property
    def fast_power_flow(self: "CastSelf") -> "FastPowerFlow":
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
class FastPowerFlow(_0.APIBase):
    """FastPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FAST_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FastPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_FastPowerFlow
        """
        return _Cast_FastPowerFlow(self)
