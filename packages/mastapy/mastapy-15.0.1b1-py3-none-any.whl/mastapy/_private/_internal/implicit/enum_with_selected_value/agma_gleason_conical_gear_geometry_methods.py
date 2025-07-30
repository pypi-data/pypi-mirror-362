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
from mastapy._private.gears.gear_designs.bevel import _1299

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods",)


class EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods

    A specific implementation of 'EnumWithSelectedValue' for 'AGMAGleasonConicalGearGeometryMethods' types.
    """

    __qualname__ = "AGMAGleasonConicalGearGeometryMethods"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods]",
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
        cls: "Type[EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods]",
    ) -> "_1299.AGMAGleasonConicalGearGeometryMethods":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1299.AGMAGleasonConicalGearGeometryMethods
        """
        return _1299.AGMAGleasonConicalGearGeometryMethods

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1299.AGMAGleasonConicalGearGeometryMethods.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1299.AGMAGleasonConicalGearGeometryMethods":
        """mastapy.gears.gear_designs.bevel.AGMAGleasonConicalGearGeometryMethods

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_1299.AGMAGleasonConicalGearGeometryMethods]":
        """List[mastapy.gears.gear_designs.bevel.AGMAGleasonConicalGearGeometryMethods]

        Note:
            This property is readonly.
        """
        return None
