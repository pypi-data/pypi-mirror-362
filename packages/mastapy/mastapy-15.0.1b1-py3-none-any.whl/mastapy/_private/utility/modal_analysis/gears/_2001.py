"""OrderWithRadius"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.modal_analysis.gears import _1999

_ORDER_WITH_RADIUS = python_net_import(
    "SMT.MastaAPI.Utility.ModalAnalysis.Gears", "OrderWithRadius"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.modal_analysis.gears import _1995, _2004

    Self = TypeVar("Self", bound="OrderWithRadius")
    CastSelf = TypeVar("CastSelf", bound="OrderWithRadius._Cast_OrderWithRadius")


__docformat__ = "restructuredtext en"
__all__ = ("OrderWithRadius",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OrderWithRadius:
    """Special nested class for casting OrderWithRadius to subclasses."""

    __parent__: "OrderWithRadius"

    @property
    def order_for_te(self: "CastSelf") -> "_1999.OrderForTE":
        return self.__parent__._cast(_1999.OrderForTE)

    @property
    def gear_order_for_te(self: "CastSelf") -> "_1995.GearOrderForTE":
        from mastapy._private.utility.modal_analysis.gears import _1995

        return self.__parent__._cast(_1995.GearOrderForTE)

    @property
    def user_defined_order_for_te(self: "CastSelf") -> "_2004.UserDefinedOrderForTE":
        from mastapy._private.utility.modal_analysis.gears import _2004

        return self.__parent__._cast(_2004.UserDefinedOrderForTE)

    @property
    def order_with_radius(self: "CastSelf") -> "OrderWithRadius":
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
class OrderWithRadius(_1999.OrderForTE):
    """OrderWithRadius

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ORDER_WITH_RADIUS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Radius")

        if temp is None:
            return 0.0

        return temp

    @radius.setter
    @exception_bridge
    @enforce_parameter_types
    def radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Radius", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_OrderWithRadius":
        """Cast to another type.

        Returns:
            _Cast_OrderWithRadius
        """
        return _Cast_OrderWithRadius(self)
