"""CustomRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1968

_CUSTOM_ROW = python_net_import("SMT.MastaAPI.Utility.Report", "CustomRow")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1939, _1982

    Self = TypeVar("Self", bound="CustomRow")
    CastSelf = TypeVar("CastSelf", bound="CustomRow._Cast_CustomRow")


__docformat__ = "restructuredtext en"
__all__ = ("CustomRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomRow:
    """Special nested class for casting CustomRow to subclasses."""

    __parent__: "CustomRow"

    @property
    def custom_report_property_item(
        self: "CastSelf",
    ) -> "_1968.CustomReportPropertyItem":
        return self.__parent__._cast(_1968.CustomReportPropertyItem)

    @property
    def blank_row(self: "CastSelf") -> "_1939.BlankRow":
        from mastapy._private.utility.report import _1939

        return self.__parent__._cast(_1939.BlankRow)

    @property
    def user_text_row(self: "CastSelf") -> "_1982.UserTextRow":
        from mastapy._private.utility.report import _1982

        return self.__parent__._cast(_1982.UserTextRow)

    @property
    def custom_row(self: "CastSelf") -> "CustomRow":
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
class CustomRow(_1968.CustomReportPropertyItem):
    """CustomRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def calculate_sum_of_values(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CalculateSumOfValues")

        if temp is None:
            return False

        return temp

    @calculate_sum_of_values.setter
    @exception_bridge
    @enforce_parameter_types
    def calculate_sum_of_values(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CalculateSumOfValues",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def count_values(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CountValues")

        if temp is None:
            return False

        return temp

    @count_values.setter
    @exception_bridge
    @enforce_parameter_types
    def count_values(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "CountValues", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def is_minor_value(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsMinorValue")

        if temp is None:
            return False

        return temp

    @is_minor_value.setter
    @exception_bridge
    @enforce_parameter_types
    def is_minor_value(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsMinorValue", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def overridden_property_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "OverriddenPropertyName")

        if temp is None:
            return ""

        return temp

    @overridden_property_name.setter
    @exception_bridge
    @enforce_parameter_types
    def overridden_property_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverriddenPropertyName",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def override_property_name(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverridePropertyName")

        if temp is None:
            return False

        return temp

    @override_property_name.setter
    @exception_bridge
    @enforce_parameter_types
    def override_property_name(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverridePropertyName",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_maximum_of_absolute_values(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowMaximumOfAbsoluteValues")

        if temp is None:
            return False

        return temp

    @show_maximum_of_absolute_values.setter
    @exception_bridge
    @enforce_parameter_types
    def show_maximum_of_absolute_values(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowMaximumOfAbsoluteValues",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_maximum_of_values(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowMaximumOfValues")

        if temp is None:
            return False

        return temp

    @show_maximum_of_values.setter
    @exception_bridge
    @enforce_parameter_types
    def show_maximum_of_values(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowMaximumOfValues",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_minimum_of_values(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowMinimumOfValues")

        if temp is None:
            return False

        return temp

    @show_minimum_of_values.setter
    @exception_bridge
    @enforce_parameter_types
    def show_minimum_of_values(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowMinimumOfValues",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_as_information(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowAsInformation")

        if temp is None:
            return False

        return temp

    @show_as_information.setter
    @exception_bridge
    @enforce_parameter_types
    def show_as_information(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowAsInformation",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomRow":
        """Cast to another type.

        Returns:
            _Cast_CustomRow
        """
        return _Cast_CustomRow(self)
