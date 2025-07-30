"""Vector6D"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility import _1710

_VECTOR_6D = python_net_import("SMT.MastaAPI.MathUtility", "Vector6D")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1698, _1709

    Self = TypeVar("Self", bound="Vector6D")
    CastSelf = TypeVar("CastSelf", bound="Vector6D._Cast_Vector6D")


__docformat__ = "restructuredtext en"
__all__ = ("Vector6D",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Vector6D:
    """Special nested class for casting Vector6D to subclasses."""

    __parent__: "Vector6D"

    @property
    def real_vector(self: "CastSelf") -> "_1710.RealVector":
        return self.__parent__._cast(_1710.RealVector)

    @property
    def real_matrix(self: "CastSelf") -> "_1709.RealMatrix":
        from mastapy._private.math_utility import _1709

        return self.__parent__._cast(_1709.RealMatrix)

    @property
    def generic_matrix(self: "CastSelf") -> "_1698.GenericMatrix":
        from mastapy._private.math_utility import _1698

        return self.__parent__._cast(_1698.GenericMatrix)

    @property
    def vector_6d(self: "CastSelf") -> "Vector6D":
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
class Vector6D(_1710.RealVector):
    """Vector6D

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VECTOR_6D

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_Vector6D":
        """Cast to another type.

        Returns:
            _Cast_Vector6D
        """
        return _Cast_Vector6D(self)
