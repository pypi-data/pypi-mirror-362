"""TaskProgress"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _7895
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.class_property import classproperty
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_STRING = python_net_import("System", "String")
_ACTION = python_net_import("System", "Action")
_TASK_PROGRESS = python_net_import("SMT.MastaAPIUtility", "TaskProgress")

if TYPE_CHECKING:
    from typing import Any, Callable, Iterable, List, Type, TypeVar

    from mastapy._private import _7902

    Self = TypeVar("Self", bound="TaskProgress")
    CastSelf = TypeVar("CastSelf", bound="TaskProgress._Cast_TaskProgress")


__docformat__ = "restructuredtext en"
__all__ = ("TaskProgress",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TaskProgress:
    """Special nested class for casting TaskProgress to subclasses."""

    __parent__: "TaskProgress"

    @property
    def task_progress(self: "CastSelf") -> "TaskProgress":
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
class TaskProgress(_7895.MarshalByRefObjectPermanent):
    """TaskProgress

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TASK_PROGRESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def title(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Title")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def status(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Status")

        if temp is None:
            return ""

        return temp

    @status.setter
    @exception_bridge
    @enforce_parameter_types
    def status(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Status", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def number_of_items(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfItems")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def show_progress(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowProgress")

        if temp is None:
            return False

        return temp

    @show_progress.setter
    @exception_bridge
    @enforce_parameter_types
    def show_progress(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowProgress", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def show_completion_status(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowCompletionStatus")

        if temp is None:
            return False

        return temp

    @show_completion_status.setter
    @exception_bridge
    @enforce_parameter_types
    def show_completion_status(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowCompletionStatus",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def can_cancel(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CanCancel")

        if temp is None:
            return False

        return temp

    @can_cancel.setter
    @exception_bridge
    @enforce_parameter_types
    def can_cancel(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "CanCancel", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def additional_string_to_add_to_title(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "AdditionalStringToAddToTitle")

        if temp is None:
            return ""

        return temp

    @additional_string_to_add_to_title.setter
    @exception_bridge
    @enforce_parameter_types
    def additional_string_to_add_to_title(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AdditionalStringToAddToTitle",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def is_progress_tree_cell_expanded(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsProgressTreeCellExpanded")

        if temp is None:
            return False

        return temp

    @is_progress_tree_cell_expanded.setter
    @exception_bridge
    @enforce_parameter_types
    def is_progress_tree_cell_expanded(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsProgressTreeCellExpanded",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def parent(self: "Self") -> "TaskProgress":
        """mastapy.TaskProgress

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Parent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @classproperty
    @exception_bridge
    def null_task_progress(cls) -> "TaskProgress":
        """mastapy.TaskProgress"""
        temp = pythonnet_property_get(TaskProgress.TYPE, "NullTaskProgress")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @classproperty
    @exception_bridge
    def null(cls) -> "TaskProgress":
        """mastapy.TaskProgress"""
        temp = pythonnet_property_get(TaskProgress.TYPE, "Null")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def child_tasks(self: "Self") -> "List[TaskProgress]":
        """List[mastapy.TaskProgress]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChildTasks")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def is_aborting(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsAborting")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def fraction_complete(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FractionComplete")

        if temp is None:
            return 0.0

        return temp

    @fraction_complete.setter
    @exception_bridge
    @enforce_parameter_types
    def fraction_complete(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FractionComplete", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def additional_status_string(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "AdditionalStatusString")

        if temp is None:
            return ""

        return temp

    @additional_status_string.setter
    @exception_bridge
    @enforce_parameter_types
    def additional_status_string(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AdditionalStatusString",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def top_parent(self: "Self") -> "TaskProgress":
        """mastapy.TaskProgress

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TopParent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def add_progress_status_updated(
        self: "Self", value: "Callable[[str], None]"
    ) -> None:
        """Method does not return.

        Args:
            value (Callable[[str], None])
        """
        pythonnet_method_call(self.wrapped, "add_ProgressStatusUpdated", value)

    @exception_bridge
    @enforce_parameter_types
    def remove_progress_status_updated(
        self: "Self", value: "Callable[[str], None]"
    ) -> None:
        """Method does not return.

        Args:
            value (Callable[[str], None])
        """
        pythonnet_method_call(self.wrapped, "remove_ProgressStatusUpdated", value)

    @exception_bridge
    @enforce_parameter_types
    def add_progress_incremented(
        self: "Self", value: "Callable[[float], None]"
    ) -> None:
        """Method does not return.

        Args:
            value (Callable[[float], None])
        """
        pythonnet_method_call(self.wrapped, "add_ProgressIncremented", value)

    @exception_bridge
    @enforce_parameter_types
    def remove_progress_incremented(
        self: "Self", value: "Callable[[float], None]"
    ) -> None:
        """Method does not return.

        Args:
            value (Callable[[float], None])
        """
        pythonnet_method_call(self.wrapped, "remove_ProgressIncremented", value)

    @exception_bridge
    def abort(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Abort")

    @exception_bridge
    @enforce_parameter_types
    def continue_with_progress(
        self: "Self",
        status_update: "str",
        perform_analysis: "Callable[[TaskProgress], None]",
    ) -> "TaskProgress":
        """mastapy.TaskProgress

        Args:
            status_update (str)
            perform_analysis (Callable[[mastapy.TaskProgress], None])
        """
        status_update = str(status_update)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ContinueWith",
            [_STRING, _ACTION[_TASK_PROGRESS]],
            status_update if status_update else "",
            perform_analysis,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def continue_with(
        self: "Self", status_update: "str", perform_analysis: "Callable[..., None]"
    ) -> "TaskProgress":
        """mastapy.TaskProgress

        Args:
            status_update (str)
            perform_analysis (Callable[..., None])
        """
        status_update = str(status_update)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ContinueWith",
            [_STRING, _ACTION],
            status_update if status_update else "",
            perform_analysis,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def get_all_errors(self: "Self") -> "Iterable[str]":
        """Iterable[str]"""
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call(self.wrapped, "GetAllErrors"), str
        )

    @exception_bridge
    @enforce_parameter_types
    def increment_progress(self: "Self", inc: "int" = 1) -> None:
        """Method does not return.

        Args:
            inc (int, optional)
        """
        inc = int(inc)
        pythonnet_method_call(self.wrapped, "IncrementProgress", inc if inc else 0)

    @exception_bridge
    @enforce_parameter_types
    def update_status_with_increment(self: "Self", new_status: "str") -> None:
        """Method does not return.

        Args:
            new_status (str)
        """
        new_status = str(new_status)
        pythonnet_method_call(
            self.wrapped, "UpdateStatusWithIncrement", new_status if new_status else ""
        )

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

    @exception_bridge
    @enforce_parameter_types
    def subdivide(self: "Self", number_of_items: "int") -> "TaskProgress":
        """mastapy.TaskProgress

        Args:
            number_of_items (int)
        """
        number_of_items = int(number_of_items)
        method_result = pythonnet_method_call(
            self.wrapped, "Subdivide", number_of_items if number_of_items else 0
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def subdivide_to_progress_with_error_handling(
        self: "Self", number_of_items: "int"
    ) -> "_7902.TaskProgressWithErrorHandling":
        """mastapy.TaskProgressWithErrorHandling

        Args:
            number_of_items (int)
        """
        number_of_items = int(number_of_items)
        method_result = pythonnet_method_call(
            self.wrapped,
            "SubdivideToProgressWithErrorHandling",
            number_of_items if number_of_items else 0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def create_new_task(
        self: "Self",
        title: "str",
        number_of_items: "int",
        show_progress: "bool" = True,
        show_eta: "bool" = False,
        manual_increment: "bool" = False,
        create_task_progess_with_error_handling: "bool" = False,
    ) -> "TaskProgress":
        """mastapy.TaskProgress

        Args:
            title (str)
            number_of_items (int)
            show_progress (bool, optional)
            show_eta (bool, optional)
            manual_increment (bool, optional)
            create_task_progess_with_error_handling (bool, optional)
        """
        title = str(title)
        number_of_items = int(number_of_items)
        show_progress = bool(show_progress)
        show_eta = bool(show_eta)
        manual_increment = bool(manual_increment)
        create_task_progess_with_error_handling = bool(
            create_task_progess_with_error_handling
        )
        method_result = pythonnet_method_call(
            self.wrapped,
            "CreateNewTask",
            title if title else "",
            number_of_items if number_of_items else 0,
            show_progress if show_progress else False,
            show_eta if show_eta else False,
            manual_increment if manual_increment else False,
            create_task_progess_with_error_handling
            if create_task_progess_with_error_handling
            else False,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def dispose(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Dispose")

    def __enter__(self: "Self") -> None:
        return self

    def __exit__(
        self: "Self", exception_type: "Any", exception_value: "Any", traceback: "Any"
    ) -> None:
        self.dispose()

    @property
    def cast_to(self: "Self") -> "_Cast_TaskProgress":
        """Cast to another type.

        Returns:
            _Cast_TaskProgress
        """
        return _Cast_TaskProgress(self)
