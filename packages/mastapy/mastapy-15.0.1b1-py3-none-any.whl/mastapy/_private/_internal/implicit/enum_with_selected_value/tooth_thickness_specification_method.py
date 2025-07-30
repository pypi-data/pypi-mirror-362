"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.bevel import _1310

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_ToothThicknessSpecificationMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ToothThicknessSpecificationMethod",)


class EnumWithSelectedValue_ToothThicknessSpecificationMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ToothThicknessSpecificationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ToothThicknessSpecificationMethod' types.
    """

    __qualname__ = "ToothThicknessSpecificationMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ToothThicknessSpecificationMethod]",
    ) -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ToothThicknessSpecificationMethod]",
    ) -> "_1310.ToothThicknessSpecificationMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1310.ToothThicknessSpecificationMethod
        """
        return _1310.ToothThicknessSpecificationMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ToothThicknessSpecificationMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1310.ToothThicknessSpecificationMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1310.ToothThicknessSpecificationMethod":
        """mastapy.gears.gear_designs.bevel.ToothThicknessSpecificationMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_1310.ToothThicknessSpecificationMethod]":
        """List[mastapy.gears.gear_designs.bevel.ToothThicknessSpecificationMethod]

        Note:
            This property is readonly.
        """
        return None
