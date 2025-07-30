"""UserDefinedOrderForTE"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.modal_analysis.gears import _2001

_USER_DEFINED_ORDER_FOR_TE = python_net_import(
    "SMT.MastaAPI.Utility.ModalAnalysis.Gears", "UserDefinedOrderForTE"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.modal_analysis.gears import _1999

    Self = TypeVar("Self", bound="UserDefinedOrderForTE")
    CastSelf = TypeVar(
        "CastSelf", bound="UserDefinedOrderForTE._Cast_UserDefinedOrderForTE"
    )


__docformat__ = "restructuredtext en"
__all__ = ("UserDefinedOrderForTE",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_UserDefinedOrderForTE:
    """Special nested class for casting UserDefinedOrderForTE to subclasses."""

    __parent__: "UserDefinedOrderForTE"

    @property
    def order_with_radius(self: "CastSelf") -> "_2001.OrderWithRadius":
        return self.__parent__._cast(_2001.OrderWithRadius)

    @property
    def order_for_te(self: "CastSelf") -> "_1999.OrderForTE":
        from mastapy._private.utility.modal_analysis.gears import _1999

        return self.__parent__._cast(_1999.OrderForTE)

    @property
    def user_defined_order_for_te(self: "CastSelf") -> "UserDefinedOrderForTE":
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
class UserDefinedOrderForTE(_2001.OrderWithRadius):
    """UserDefinedOrderForTE

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _USER_DEFINED_ORDER_FOR_TE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_UserDefinedOrderForTE":
        """Cast to another type.

        Returns:
            _Cast_UserDefinedOrderForTE
        """
        return _Cast_UserDefinedOrderForTE(self)
