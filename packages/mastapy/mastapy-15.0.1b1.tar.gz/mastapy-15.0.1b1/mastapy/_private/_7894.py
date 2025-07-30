"""ConsoleProgress"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _7901
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CONSOLE_PROGRESS = python_net_import("SMT.MastaAPIUtility", "ConsoleProgress")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConsoleProgress")
    CastSelf = TypeVar("CastSelf", bound="ConsoleProgress._Cast_ConsoleProgress")


__docformat__ = "restructuredtext en"
__all__ = ("ConsoleProgress",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConsoleProgress:
    """Special nested class for casting ConsoleProgress to subclasses."""

    __parent__: "ConsoleProgress"

    @property
    def console_progress(self: "CastSelf") -> "ConsoleProgress":
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
class ConsoleProgress(_7901.TaskProgress):
    """ConsoleProgress

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONSOLE_PROGRESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Id")

        if temp is None:
            return 0

        return temp

    @exception_bridge
    @enforce_parameter_types
    def add_error(self: "Self", error: "str") -> None:
        """Method does not return.

        Args:
            error (str)
        """
        error = str(error)
        pythonnet_method_call(self.wrapped, "AddError", error if error else "")

    @exception_bridge
    def complete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Complete")

    @property
    def cast_to(self: "Self") -> "_Cast_ConsoleProgress":
        """Cast to another type.

        Returns:
            _Cast_ConsoleProgress
        """
        return _Cast_ConsoleProgress(self)
