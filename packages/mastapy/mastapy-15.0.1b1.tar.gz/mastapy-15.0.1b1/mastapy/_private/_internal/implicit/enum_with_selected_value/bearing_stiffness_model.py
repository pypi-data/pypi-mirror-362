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
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5670

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_BearingStiffnessModel")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_BearingStiffnessModel",)


class EnumWithSelectedValue_BearingStiffnessModel(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_BearingStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'BearingStiffnessModel' types.
    """

    __qualname__ = "BearingStiffnessModel"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_BearingStiffnessModel]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_BearingStiffnessModel]",
    ) -> "_5670.BearingStiffnessModel":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _5670.BearingStiffnessModel
        """
        return _5670.BearingStiffnessModel

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_BearingStiffnessModel]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _5670.BearingStiffnessModel.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_5670.BearingStiffnessModel":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BearingStiffnessModel

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_5670.BearingStiffnessModel]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.BearingStiffnessModel]

        Note:
            This property is readonly.
        """
        return None
