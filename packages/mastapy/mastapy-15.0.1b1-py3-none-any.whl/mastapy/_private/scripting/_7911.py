"""ScriptingCommand"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _7895
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)

_SCRIPTING_COMMAND = python_net_import(
    "SMT.MastaAPIUtility.Scripting", "ScriptingCommand"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ScriptingCommand")
    CastSelf = TypeVar("CastSelf", bound="ScriptingCommand._Cast_ScriptingCommand")


__docformat__ = "restructuredtext en"
__all__ = ("ScriptingCommand",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ScriptingCommand:
    """Special nested class for casting ScriptingCommand to subclasses."""

    __parent__: "ScriptingCommand"

    @property
    def scripting_command(self: "CastSelf") -> "ScriptingCommand":
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
class ScriptingCommand(_7895.MarshalByRefObjectPermanent):
    """ScriptingCommand

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SCRIPTING_COMMAND

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
    def cast_to(self: "Self") -> "_Cast_ScriptingCommand":
        """Cast to another type.

        Returns:
            _Cast_ScriptingCommand
        """
        return _Cast_ScriptingCommand(self)
