"""SparseNodalMatrix"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis import _50

_SPARSE_NODAL_MATRIX = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "SparseNodalMatrix"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SparseNodalMatrix")
    CastSelf = TypeVar("CastSelf", bound="SparseNodalMatrix._Cast_SparseNodalMatrix")


__docformat__ = "restructuredtext en"
__all__ = ("SparseNodalMatrix",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SparseNodalMatrix:
    """Special nested class for casting SparseNodalMatrix to subclasses."""

    __parent__: "SparseNodalMatrix"

    @property
    def abstract_nodal_matrix(self: "CastSelf") -> "_50.AbstractNodalMatrix":
        return self.__parent__._cast(_50.AbstractNodalMatrix)

    @property
    def sparse_nodal_matrix(self: "CastSelf") -> "SparseNodalMatrix":
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
class SparseNodalMatrix(_50.AbstractNodalMatrix):
    """SparseNodalMatrix

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPARSE_NODAL_MATRIX

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SparseNodalMatrix":
        """Cast to another type.

        Returns:
            _Cast_SparseNodalMatrix
        """
        return _Cast_SparseNodalMatrix(self)
