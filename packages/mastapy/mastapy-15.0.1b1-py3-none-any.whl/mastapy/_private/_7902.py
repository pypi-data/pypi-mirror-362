"""TaskProgressWithErrorHandling"""

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
)

_TASK_PROGRESS_WITH_ERROR_HANDLING = python_net_import(
    "SMT.MastaAPIUtility", "TaskProgressWithErrorHandling"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TaskProgressWithErrorHandling")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TaskProgressWithErrorHandling._Cast_TaskProgressWithErrorHandling",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TaskProgressWithErrorHandling",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TaskProgressWithErrorHandling:
    """Special nested class for casting TaskProgressWithErrorHandling to subclasses."""

    __parent__: "TaskProgressWithErrorHandling"

    @property
    def task_progress_with_error_handling(
        self: "CastSelf",
    ) -> "TaskProgressWithErrorHandling":
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
class TaskProgressWithErrorHandling(_7901.TaskProgress):
    """TaskProgressWithErrorHandling

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TASK_PROGRESS_WITH_ERROR_HANDLING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    def error_occurred(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ErrorOccurred")

    @property
    def cast_to(self: "Self") -> "_Cast_TaskProgressWithErrorHandling":
        """Cast to another type.

        Returns:
            _Cast_TaskProgressWithErrorHandling
        """
        return _Cast_TaskProgressWithErrorHandling(self)
