"""ConvergenceLogger"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility.convergence import _1760

_CONVERGENCE_LOGGER = python_net_import(
    "SMT.MastaAPI.MathUtility.Convergence", "ConvergenceLogger"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConvergenceLogger")
    CastSelf = TypeVar("CastSelf", bound="ConvergenceLogger._Cast_ConvergenceLogger")


__docformat__ = "restructuredtext en"
__all__ = ("ConvergenceLogger",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConvergenceLogger:
    """Special nested class for casting ConvergenceLogger to subclasses."""

    __parent__: "ConvergenceLogger"

    @property
    def data_logger(self: "CastSelf") -> "_1760.DataLogger":
        return self.__parent__._cast(_1760.DataLogger)

    @property
    def convergence_logger(self: "CastSelf") -> "ConvergenceLogger":
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
class ConvergenceLogger(_1760.DataLogger):
    """ConvergenceLogger

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONVERGENCE_LOGGER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConvergenceLogger":
        """Cast to another type.

        Returns:
            _Cast_ConvergenceLogger
        """
        return _Cast_ConvergenceLogger(self)
