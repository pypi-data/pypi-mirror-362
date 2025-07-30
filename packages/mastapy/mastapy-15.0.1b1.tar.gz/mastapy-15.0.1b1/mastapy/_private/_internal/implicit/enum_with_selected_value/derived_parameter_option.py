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
from mastapy._private.gears.gear_designs.creation_options import _1265

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self",
        bound="EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption",
    )


__docformat__ = "restructuredtext en"
__all__ = (
    "EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption",
)


class EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalGearPairCreationOptions.DerivedParameterOption' types.
    """

    __qualname__ = "CylindricalGearPairCreationOptions.DerivedParameterOption"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption]",
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
        cls: "Type[EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption]",
    ) -> "_1265.CylindricalGearPairCreationOptions.DerivedParameterOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1265.CylindricalGearPairCreationOptions.DerivedParameterOption
        """
        return _1265.CylindricalGearPairCreationOptions.DerivedParameterOption

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1265.CylindricalGearPairCreationOptions.DerivedParameterOption.type_()

    @property
    @exception_bridge
    def selected_value(
        self: "Self",
    ) -> "_1265.CylindricalGearPairCreationOptions.DerivedParameterOption":
        """mastapy.gears.gear_designs.creation_options.CylindricalGearPairCreationOptions.DerivedParameterOption

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_1265.CylindricalGearPairCreationOptions.DerivedParameterOption]":
        """List[mastapy.gears.gear_designs.creation_options.CylindricalGearPairCreationOptions.DerivedParameterOption]

        Note:
            This property is readonly.
        """
        return None
