"""Quaternion"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility import _1710

_QUATERNION = python_net_import("SMT.MastaAPI.MathUtility", "Quaternion")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1698, _1709

    Self = TypeVar("Self", bound="Quaternion")
    CastSelf = TypeVar("CastSelf", bound="Quaternion._Cast_Quaternion")


__docformat__ = "restructuredtext en"
__all__ = ("Quaternion",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Quaternion:
    """Special nested class for casting Quaternion to subclasses."""

    __parent__: "Quaternion"

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
    def quaternion(self: "CastSelf") -> "Quaternion":
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
class Quaternion(_1710.RealVector):
    """Quaternion

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _QUATERNION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_Quaternion":
        """Cast to another type.

        Returns:
            _Cast_Quaternion
        """
        return _Cast_Quaternion(self)
