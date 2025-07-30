"""OrderSelector"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.modal_analysis.gears import _1999

_ORDER_SELECTOR = python_net_import(
    "SMT.MastaAPI.Utility.ModalAnalysis.Gears", "OrderSelector"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OrderSelector")
    CastSelf = TypeVar("CastSelf", bound="OrderSelector._Cast_OrderSelector")


__docformat__ = "restructuredtext en"
__all__ = ("OrderSelector",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OrderSelector:
    """Special nested class for casting OrderSelector to subclasses."""

    __parent__: "OrderSelector"

    @property
    def order_for_te(self: "CastSelf") -> "_1999.OrderForTE":
        return self.__parent__._cast(_1999.OrderForTE)

    @property
    def order_selector(self: "CastSelf") -> "OrderSelector":
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
class OrderSelector(_1999.OrderForTE):
    """OrderSelector

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ORDER_SELECTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_OrderSelector":
        """Cast to another type.

        Returns:
            _Cast_OrderSelector
        """
        return _Cast_OrderSelector(self)
