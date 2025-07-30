"""GreaseQuantity"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling.skf_module import _2305

_GREASE_QUANTITY = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "GreaseQuantity"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GreaseQuantity")
    CastSelf = TypeVar("CastSelf", bound="GreaseQuantity._Cast_GreaseQuantity")


__docformat__ = "restructuredtext en"
__all__ = ("GreaseQuantity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GreaseQuantity:
    """Special nested class for casting GreaseQuantity to subclasses."""

    __parent__: "GreaseQuantity"

    @property
    def skf_calculation_result(self: "CastSelf") -> "_2305.SKFCalculationResult":
        return self.__parent__._cast(_2305.SKFCalculationResult)

    @property
    def grease_quantity(self: "CastSelf") -> "GreaseQuantity":
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
class GreaseQuantity(_2305.SKFCalculationResult):
    """GreaseQuantity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GREASE_QUANTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Ring")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Side")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GreaseQuantity":
        """Cast to another type.

        Returns:
            _Cast_GreaseQuantity
        """
        return _Cast_GreaseQuantity(self)
