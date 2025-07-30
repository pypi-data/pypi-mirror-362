"""RoundedOrder"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_ROUNDED_ORDER = python_net_import("SMT.MastaAPI.MathUtility", "RoundedOrder")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RoundedOrder")
    CastSelf = TypeVar("CastSelf", bound="RoundedOrder._Cast_RoundedOrder")


__docformat__ = "restructuredtext en"
__all__ = ("RoundedOrder",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RoundedOrder:
    """Special nested class for casting RoundedOrder to subclasses."""

    __parent__: "RoundedOrder"

    @property
    def rounded_order(self: "CastSelf") -> "RoundedOrder":
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
class RoundedOrder(_0.APIBase):
    """RoundedOrder

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROUNDED_ORDER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RoundedOrder":
        """Cast to another type.

        Returns:
            _Cast_RoundedOrder
        """
        return _Cast_RoundedOrder(self)
