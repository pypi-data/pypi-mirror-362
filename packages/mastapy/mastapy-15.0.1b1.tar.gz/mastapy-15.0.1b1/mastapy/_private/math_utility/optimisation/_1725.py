"""Optimisable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility.optimisation import _1722

_OPTIMISABLE = python_net_import("SMT.MastaAPI.MathUtility.Optimisation", "Optimisable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Optimisable")
    CastSelf = TypeVar("CastSelf", bound="Optimisable._Cast_Optimisable")


__docformat__ = "restructuredtext en"
__all__ = ("Optimisable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Optimisable:
    """Special nested class for casting Optimisable to subclasses."""

    __parent__: "Optimisable"

    @property
    def abstract_optimisable(self: "CastSelf") -> "_1722.AbstractOptimisable":
        return self.__parent__._cast(_1722.AbstractOptimisable)

    @property
    def optimisable(self: "CastSelf") -> "Optimisable":
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
class Optimisable(_1722.AbstractOptimisable):
    """Optimisable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OPTIMISABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_Optimisable":
        """Cast to another type.

        Returns:
            _Cast_Optimisable
        """
        return _Cast_Optimisable(self)
