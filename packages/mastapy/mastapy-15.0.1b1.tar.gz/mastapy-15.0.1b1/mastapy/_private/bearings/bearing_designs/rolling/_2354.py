"""BearingProtectionDetailsModifier"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_BEARING_PROTECTION_DETAILS_MODIFIER = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "BearingProtectionDetailsModifier"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings.bearing_designs.rolling import _2355

    Self = TypeVar("Self", bound="BearingProtectionDetailsModifier")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BearingProtectionDetailsModifier._Cast_BearingProtectionDetailsModifier",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingProtectionDetailsModifier",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingProtectionDetailsModifier:
    """Special nested class for casting BearingProtectionDetailsModifier to subclasses."""

    __parent__: "BearingProtectionDetailsModifier"

    @property
    def bearing_protection_details_modifier(
        self: "CastSelf",
    ) -> "BearingProtectionDetailsModifier":
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
class BearingProtectionDetailsModifier(_0.APIBase):
    """BearingProtectionDetailsModifier

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_PROTECTION_DETAILS_MODIFIER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def confirm_new_password(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "ConfirmNewPassword")

        if temp is None:
            return ""

        return temp

    @confirm_new_password.setter
    @exception_bridge
    @enforce_parameter_types
    def confirm_new_password(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "ConfirmNewPassword", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def current_password(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "CurrentPassword")

        if temp is None:
            return ""

        return temp

    @current_password.setter
    @exception_bridge
    @enforce_parameter_types
    def current_password(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "CurrentPassword", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def current_protection_level(self: "Self") -> "_2355.BearingProtectionLevel":
        """mastapy.bearings.bearing_designs.rolling.BearingProtectionLevel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentProtectionLevel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.BearingProtectionLevel"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_designs.rolling._2355",
            "BearingProtectionLevel",
        )(value)

    @property
    @exception_bridge
    def new_password(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "NewPassword")

        if temp is None:
            return ""

        return temp

    @new_password.setter
    @exception_bridge
    @enforce_parameter_types
    def new_password(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "NewPassword", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def new_protection_level(self: "Self") -> "_2355.BearingProtectionLevel":
        """mastapy.bearings.bearing_designs.rolling.BearingProtectionLevel"""
        temp = pythonnet_property_get(self.wrapped, "NewProtectionLevel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.BearingProtectionLevel"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_designs.rolling._2355",
            "BearingProtectionLevel",
        )(value)

    @new_protection_level.setter
    @exception_bridge
    @enforce_parameter_types
    def new_protection_level(
        self: "Self", value: "_2355.BearingProtectionLevel"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.BearingProtectionLevel"
        )
        pythonnet_property_set(self.wrapped, "NewProtectionLevel", value)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_BearingProtectionDetailsModifier":
        """Cast to another type.

        Returns:
            _Cast_BearingProtectionDetailsModifier
        """
        return _Cast_BearingProtectionDetailsModifier(self)
