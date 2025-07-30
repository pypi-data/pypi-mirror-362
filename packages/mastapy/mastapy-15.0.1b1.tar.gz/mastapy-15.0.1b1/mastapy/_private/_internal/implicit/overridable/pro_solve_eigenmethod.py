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
from mastapy._private.fe_tools.vfx_tools.vfx_enums import _1360

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_ProSolveEigenmethod")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_ProSolveEigenmethod",)


class Overridable_ProSolveEigenmethod(mixins.OverridableMixin, Enum):
    """Overridable_ProSolveEigenmethod

    A specific implementation of 'Overridable' for 'ProSolveEigenmethod' types.
    """

    __qualname__ = "ProSolveEigenmethod"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_ProSolveEigenmethod]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_ProSolveEigenmethod]",
    ) -> "_1360.ProSolveEigenmethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1360.ProSolveEigenmethod
        """
        return _1360.ProSolveEigenmethod

    @classmethod
    def implicit_type(cls: "Type[Overridable_ProSolveEigenmethod]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1360.ProSolveEigenmethod.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_1360.ProSolveEigenmethod":
        """mastapy.fe_tools.vfx_tools.vfx_enums.ProSolveEigenmethod

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
    def override_value(self: "Self") -> "_1360.ProSolveEigenmethod":
        """mastapy.fe_tools.vfx_tools.vfx_enums.ProSolveEigenmethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_1360.ProSolveEigenmethod":
        """mastapy.fe_tools.vfx_tools.vfx_enums.ProSolveEigenmethod

        Note:
            This property is readonly.
        """
        return None
