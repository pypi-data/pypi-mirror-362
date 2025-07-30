"""NodalMatrix"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.nodal_analysis import _50

_NODAL_MATRIX = python_net_import("SMT.MastaAPI.NodalAnalysis", "NodalMatrix")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis import _86

    Self = TypeVar("Self", bound="NodalMatrix")
    CastSelf = TypeVar("CastSelf", bound="NodalMatrix._Cast_NodalMatrix")


__docformat__ = "restructuredtext en"
__all__ = ("NodalMatrix",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodalMatrix:
    """Special nested class for casting NodalMatrix to subclasses."""

    __parent__: "NodalMatrix"

    @property
    def abstract_nodal_matrix(self: "CastSelf") -> "_50.AbstractNodalMatrix":
        return self.__parent__._cast(_50.AbstractNodalMatrix)

    @property
    def nodal_matrix(self: "CastSelf") -> "NodalMatrix":
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
class NodalMatrix(_50.AbstractNodalMatrix):
    """NodalMatrix

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODAL_MATRIX

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def rows(self: "Self") -> "List[_86.NodalMatrixRow]":
        """List[mastapy.nodal_analysis.NodalMatrixRow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rows")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_NodalMatrix":
        """Cast to another type.

        Returns:
            _Cast_NodalMatrix
        """
        return _Cast_NodalMatrix(self)
