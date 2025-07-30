"""RealVector"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility import _1709

_REAL_VECTOR = python_net_import("SMT.MastaAPI.MathUtility", "RealVector")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1693, _1698, _1708, _1719

    Self = TypeVar("Self", bound="RealVector")
    CastSelf = TypeVar("CastSelf", bound="RealVector._Cast_RealVector")


__docformat__ = "restructuredtext en"
__all__ = ("RealVector",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RealVector:
    """Special nested class for casting RealVector to subclasses."""

    __parent__: "RealVector"

    @property
    def real_matrix(self: "CastSelf") -> "_1709.RealMatrix":
        return self.__parent__._cast(_1709.RealMatrix)

    @property
    def generic_matrix(self: "CastSelf") -> "_1698.GenericMatrix":
        from mastapy._private.math_utility import _1698

        return self.__parent__._cast(_1698.GenericMatrix)

    @property
    def euler_parameters(self: "CastSelf") -> "_1693.EulerParameters":
        from mastapy._private.math_utility import _1693

        return self.__parent__._cast(_1693.EulerParameters)

    @property
    def quaternion(self: "CastSelf") -> "_1708.Quaternion":
        from mastapy._private.math_utility import _1708

        return self.__parent__._cast(_1708.Quaternion)

    @property
    def vector_6d(self: "CastSelf") -> "_1719.Vector6D":
        from mastapy._private.math_utility import _1719

        return self.__parent__._cast(_1719.Vector6D)

    @property
    def real_vector(self: "CastSelf") -> "RealVector":
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
class RealVector(_1709.RealMatrix):
    """RealVector

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REAL_VECTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RealVector":
        """Cast to another type.

        Returns:
            _Cast_RealVector
        """
        return _Cast_RealVector(self)
