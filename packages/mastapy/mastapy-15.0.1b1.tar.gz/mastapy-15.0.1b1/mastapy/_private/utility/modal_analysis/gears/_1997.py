"""HarmonicOrderForTE"""

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
from mastapy._private.utility.modal_analysis.gears import _1999

_HARMONIC_ORDER_FOR_TE = python_net_import(
    "SMT.MastaAPI.Utility.ModalAnalysis.Gears", "HarmonicOrderForTE"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HarmonicOrderForTE")
    CastSelf = TypeVar("CastSelf", bound="HarmonicOrderForTE._Cast_HarmonicOrderForTE")


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicOrderForTE",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicOrderForTE:
    """Special nested class for casting HarmonicOrderForTE to subclasses."""

    __parent__: "HarmonicOrderForTE"

    @property
    def order_for_te(self: "CastSelf") -> "_1999.OrderForTE":
        return self.__parent__._cast(_1999.OrderForTE)

    @property
    def harmonic_order_for_te(self: "CastSelf") -> "HarmonicOrderForTE":
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
class HarmonicOrderForTE(_1999.OrderForTE):
    """HarmonicOrderForTE

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ORDER_FOR_TE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def harmonic(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Harmonic")

        if temp is None:
            return 0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicOrderForTE":
        """Cast to another type.

        Returns:
            _Cast_HarmonicOrderForTE
        """
        return _Cast_HarmonicOrderForTE(self)
