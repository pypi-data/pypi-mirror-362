"""NodalMatrixRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_NODAL_MATRIX_ROW = python_net_import("SMT.MastaAPI.NodalAnalysis", "NodalMatrixRow")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="NodalMatrixRow")
    CastSelf = TypeVar("CastSelf", bound="NodalMatrixRow._Cast_NodalMatrixRow")


__docformat__ = "restructuredtext en"
__all__ = ("NodalMatrixRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodalMatrixRow:
    """Special nested class for casting NodalMatrixRow to subclasses."""

    __parent__: "NodalMatrixRow"

    @property
    def nodal_matrix_row(self: "CastSelf") -> "NodalMatrixRow":
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
class NodalMatrixRow(_0.APIBase):
    """NodalMatrixRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODAL_MATRIX_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def comma_separated_values(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CommaSeparatedValues")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def degree_of_freedom(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DegreeOfFreedom")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def node_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeIndex")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def values(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Values")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_NodalMatrixRow":
        """Cast to another type.

        Returns:
            _Cast_NodalMatrixRow
        """
        return _Cast_NodalMatrixRow(self)
