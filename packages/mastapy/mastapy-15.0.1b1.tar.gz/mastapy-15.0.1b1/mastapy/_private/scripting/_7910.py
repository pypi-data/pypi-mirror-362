"""PythonCommand"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private.scripting import _7911

_PYTHON_COMMAND = python_net_import("SMT.MastaAPIUtility.Scripting", "PythonCommand")

if TYPE_CHECKING:
    from typing import Any, Type

    Self = TypeVar("Self", bound="PythonCommand")
    CastSelf = TypeVar("CastSelf", bound="PythonCommand._Cast_PythonCommand")

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("PythonCommand",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PythonCommand:
    """Special nested class for casting PythonCommand to subclasses."""

    __parent__: "PythonCommand"

    @property
    def python_command(self: "CastSelf") -> "PythonCommand":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class PythonCommand(_7911.ScriptingCommand, Generic[T]):
    """PythonCommand

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _PYTHON_COMMAND

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    def execute(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Execute")

    @property
    def cast_to(self: "Self") -> "_Cast_PythonCommand":
        """Cast to another type.

        Returns:
            _Cast_PythonCommand
        """
        return _Cast_PythonCommand(self)
