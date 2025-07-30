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
from mastapy._private.gears.gear_designs.conical import _1277

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_ConicalMachineSettingCalculationMethods"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ConicalMachineSettingCalculationMethods",)


class EnumWithSelectedValue_ConicalMachineSettingCalculationMethods(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ConicalMachineSettingCalculationMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ConicalMachineSettingCalculationMethods' types.
    """

    __qualname__ = "ConicalMachineSettingCalculationMethods"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ConicalMachineSettingCalculationMethods]",
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
        cls: "Type[EnumWithSelectedValue_ConicalMachineSettingCalculationMethods]",
    ) -> "_1277.ConicalMachineSettingCalculationMethods":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1277.ConicalMachineSettingCalculationMethods
        """
        return _1277.ConicalMachineSettingCalculationMethods

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ConicalMachineSettingCalculationMethods]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1277.ConicalMachineSettingCalculationMethods.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1277.ConicalMachineSettingCalculationMethods":
        """mastapy.gears.gear_designs.conical.ConicalMachineSettingCalculationMethods

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_1277.ConicalMachineSettingCalculationMethods]":
        """List[mastapy.gears.gear_designs.conical.ConicalMachineSettingCalculationMethods]

        Note:
            This property is readonly.
        """
        return None
