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
from mastapy._private.system_model import _2428

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod",)


class EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'PowerLoadInputTorqueSpecificationMethod' types.
    """

    __qualname__ = "PowerLoadInputTorqueSpecificationMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod]",
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
        cls: "Type[EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod]",
    ) -> "_2428.PowerLoadInputTorqueSpecificationMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2428.PowerLoadInputTorqueSpecificationMethod
        """
        return _2428.PowerLoadInputTorqueSpecificationMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2428.PowerLoadInputTorqueSpecificationMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2428.PowerLoadInputTorqueSpecificationMethod":
        """mastapy.system_model.PowerLoadInputTorqueSpecificationMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_2428.PowerLoadInputTorqueSpecificationMethod]":
        """List[mastapy.system_model.PowerLoadInputTorqueSpecificationMethod]

        Note:
            This property is readonly.
        """
        return None
