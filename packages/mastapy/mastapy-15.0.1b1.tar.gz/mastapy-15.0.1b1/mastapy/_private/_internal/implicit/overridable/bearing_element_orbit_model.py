"""Implementations of 'Overridable' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5668

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_BearingElementOrbitModel")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_BearingElementOrbitModel",)


class Overridable_BearingElementOrbitModel(mixins.OverridableMixin, Enum):
    """Overridable_BearingElementOrbitModel

    A specific implementation of 'Overridable' for 'BearingElementOrbitModel' types.
    """

    __qualname__ = "BearingElementOrbitModel"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_BearingElementOrbitModel]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_BearingElementOrbitModel]",
    ) -> "_5668.BearingElementOrbitModel":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _5668.BearingElementOrbitModel
        """
        return _5668.BearingElementOrbitModel

    @classmethod
    def implicit_type(cls: "Type[Overridable_BearingElementOrbitModel]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _5668.BearingElementOrbitModel.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_5668.BearingElementOrbitModel":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BearingElementOrbitModel

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def overridden(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def override_value(self: "Self") -> "_5668.BearingElementOrbitModel":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BearingElementOrbitModel

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_5668.BearingElementOrbitModel":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BearingElementOrbitModel

        Note:
            This property is readonly.
        """
        return None
