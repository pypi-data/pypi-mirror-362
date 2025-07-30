"""ComplexVector3D"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility import _1680

_COMPLEX_VECTOR_3D = python_net_import("SMT.MastaAPI.MathUtility", "ComplexVector3D")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1678, _1698

    Self = TypeVar("Self", bound="ComplexVector3D")
    CastSelf = TypeVar("CastSelf", bound="ComplexVector3D._Cast_ComplexVector3D")


__docformat__ = "restructuredtext en"
__all__ = ("ComplexVector3D",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComplexVector3D:
    """Special nested class for casting ComplexVector3D to subclasses."""

    __parent__: "ComplexVector3D"

    @property
    def complex_vector(self: "CastSelf") -> "_1680.ComplexVector":
        return self.__parent__._cast(_1680.ComplexVector)

    @property
    def complex_matrix(self: "CastSelf") -> "_1678.ComplexMatrix":
        from mastapy._private.math_utility import _1678

        return self.__parent__._cast(_1678.ComplexMatrix)

    @property
    def generic_matrix(self: "CastSelf") -> "_1698.GenericMatrix":
        from mastapy._private.math_utility import _1698

        return self.__parent__._cast(_1698.GenericMatrix)

    @property
    def complex_vector_3d(self: "CastSelf") -> "ComplexVector3D":
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
class ComplexVector3D(_1680.ComplexVector):
    """ComplexVector3D

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPLEX_VECTOR_3D

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ComplexVector3D":
        """Cast to another type.

        Returns:
            _Cast_ComplexVector3D
        """
        return _Cast_ComplexVector3D(self)
