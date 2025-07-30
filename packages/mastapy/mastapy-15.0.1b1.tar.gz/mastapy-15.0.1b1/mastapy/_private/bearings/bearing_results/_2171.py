"""StiffnessRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_STIFFNESS_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "StiffnessRow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="StiffnessRow")
    CastSelf = TypeVar("CastSelf", bound="StiffnessRow._Cast_StiffnessRow")


__docformat__ = "restructuredtext en"
__all__ = ("StiffnessRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StiffnessRow:
    """Special nested class for casting StiffnessRow to subclasses."""

    __parent__: "StiffnessRow"

    @property
    def stiffness_row(self: "CastSelf") -> "StiffnessRow":
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
class StiffnessRow(_0.APIBase):
    """StiffnessRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STIFFNESS_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def comma_separated_values_mn_rad(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CommaSeparatedValuesMNRad")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def row_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RowIndex")

        if temp is None:
            return 0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_StiffnessRow":
        """Cast to another type.

        Returns:
            _Cast_StiffnessRow
        """
        return _Cast_StiffnessRow(self)
