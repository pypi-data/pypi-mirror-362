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
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5770

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_ShaftAndHousingFlexibilityOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ShaftAndHousingFlexibilityOption",)


class EnumWithSelectedValue_ShaftAndHousingFlexibilityOption(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ShaftAndHousingFlexibilityOption

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftAndHousingFlexibilityOption' types.
    """

    __qualname__ = "ShaftAndHousingFlexibilityOption"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ShaftAndHousingFlexibilityOption]",
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
        cls: "Type[EnumWithSelectedValue_ShaftAndHousingFlexibilityOption]",
    ) -> "_5770.ShaftAndHousingFlexibilityOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _5770.ShaftAndHousingFlexibilityOption
        """
        return _5770.ShaftAndHousingFlexibilityOption

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ShaftAndHousingFlexibilityOption]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _5770.ShaftAndHousingFlexibilityOption.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_5770.ShaftAndHousingFlexibilityOption":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ShaftAndHousingFlexibilityOption

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_5770.ShaftAndHousingFlexibilityOption]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.ShaftAndHousingFlexibilityOption]

        Note:
            This property is readonly.
        """
        return None
