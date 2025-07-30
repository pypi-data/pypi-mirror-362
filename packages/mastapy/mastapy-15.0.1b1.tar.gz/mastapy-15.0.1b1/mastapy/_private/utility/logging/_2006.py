"""Message"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_MESSAGE = python_net_import("SMT.MastaAPI.Utility.Logging", "Message")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Message")
    CastSelf = TypeVar("CastSelf", bound="Message._Cast_Message")


__docformat__ = "restructuredtext en"
__all__ = ("Message",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Message:
    """Special nested class for casting Message to subclasses."""

    __parent__: "Message"

    @property
    def message(self: "CastSelf") -> "Message":
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
class Message(_0.APIBase):
    """Message

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MESSAGE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def text(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Text")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def verbose(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Verbose")

        if temp is None:
            return False

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_Message":
        """Cast to another type.

        Returns:
            _Cast_Message
        """
        return _Cast_Message(self)
