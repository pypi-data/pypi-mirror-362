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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6081

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ModalCorrectionMethod")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ModalCorrectionMethod",)


class EnumWithSelectedValue_ModalCorrectionMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ModalCorrectionMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ModalCorrectionMethod' types.
    """

    __qualname__ = "ModalCorrectionMethod"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ModalCorrectionMethod]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ModalCorrectionMethod]",
    ) -> "_6081.ModalCorrectionMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _6081.ModalCorrectionMethod
        """
        return _6081.ModalCorrectionMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ModalCorrectionMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _6081.ModalCorrectionMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_6081.ModalCorrectionMethod":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.ModalCorrectionMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_6081.ModalCorrectionMethod]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ModalCorrectionMethod]

        Note:
            This property is readonly.
        """
        return None
