"""UserTextRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1973

_USER_TEXT_ROW = python_net_import("SMT.MastaAPI.Utility.Report", "UserTextRow")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1968, _1980

    Self = TypeVar("Self", bound="UserTextRow")
    CastSelf = TypeVar("CastSelf", bound="UserTextRow._Cast_UserTextRow")


__docformat__ = "restructuredtext en"
__all__ = ("UserTextRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_UserTextRow:
    """Special nested class for casting UserTextRow to subclasses."""

    __parent__: "UserTextRow"

    @property
    def custom_row(self: "CastSelf") -> "_1973.CustomRow":
        return self.__parent__._cast(_1973.CustomRow)

    @property
    def custom_report_property_item(
        self: "CastSelf",
    ) -> "_1968.CustomReportPropertyItem":
        from mastapy._private.utility.report import _1968

        return self.__parent__._cast(_1968.CustomReportPropertyItem)

    @property
    def user_text_row(self: "CastSelf") -> "UserTextRow":
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
class UserTextRow(_1973.CustomRow):
    """UserTextRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _USER_TEXT_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def additional_text(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "AdditionalText")

        if temp is None:
            return ""

        return temp

    @additional_text.setter
    @exception_bridge
    @enforce_parameter_types
    def additional_text(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "AdditionalText", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def heading_size(self: "Self") -> "_1980.HeadingSize":
        """mastapy.utility.report.HeadingSize"""
        temp = pythonnet_property_get(self.wrapped, "HeadingSize")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.Report.HeadingSize"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.report._1980", "HeadingSize"
        )(value)

    @heading_size.setter
    @exception_bridge
    @enforce_parameter_types
    def heading_size(self: "Self", value: "_1980.HeadingSize") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.Report.HeadingSize"
        )
        pythonnet_property_set(self.wrapped, "HeadingSize", value)

    @property
    @exception_bridge
    def is_heading(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsHeading")

        if temp is None:
            return False

        return temp

    @is_heading.setter
    @exception_bridge
    @enforce_parameter_types
    def is_heading(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsHeading", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def show_additional_text(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowAdditionalText")

        if temp is None:
            return False

        return temp

    @show_additional_text.setter
    @exception_bridge
    @enforce_parameter_types
    def show_additional_text(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowAdditionalText",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def text(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Text")

        if temp is None:
            return ""

        return temp

    @text.setter
    @exception_bridge
    @enforce_parameter_types
    def text(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Text", str(value) if value is not None else ""
        )

    @property
    def cast_to(self: "Self") -> "_Cast_UserTextRow":
        """Cast to another type.

        Returns:
            _Cast_UserTextRow
        """
        return _Cast_UserTextRow(self)
