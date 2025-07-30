"""NotchSpecification"""

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

_NOTCH_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "NotchSpecification"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import _1422

    Self = TypeVar("Self", bound="NotchSpecification")
    CastSelf = TypeVar("CastSelf", bound="NotchSpecification._Cast_NotchSpecification")


__docformat__ = "restructuredtext en"
__all__ = ("NotchSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NotchSpecification:
    """Special nested class for casting NotchSpecification to subclasses."""

    __parent__: "NotchSpecification"

    @property
    def notch_specification(self: "CastSelf") -> "NotchSpecification":
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
class NotchSpecification(_0.APIBase):
    """NotchSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NOTCH_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def first_notch_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstNotchAngle")

        if temp is None:
            return 0.0

        return temp

    @first_notch_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def first_notch_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FirstNotchAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def notch_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NotchDepth")

        if temp is None:
            return 0.0

        return temp

    @notch_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def notch_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NotchDepth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def notch_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NotchDiameter")

        if temp is None:
            return 0.0

        return temp

    @notch_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def notch_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NotchDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def notch_offset_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NotchOffsetFactor")

        if temp is None:
            return 0.0

        return temp

    @notch_offset_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def notch_offset_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NotchOffsetFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def notch_shape(self: "Self") -> "_1422.NotchShape":
        """mastapy.electric_machines.NotchShape"""
        temp = pythonnet_property_get(self.wrapped, "NotchShape")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.NotchShape"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1422", "NotchShape"
        )(value)

    @notch_shape.setter
    @exception_bridge
    @enforce_parameter_types
    def notch_shape(self: "Self", value: "_1422.NotchShape") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.NotchShape"
        )
        pythonnet_property_set(self.wrapped, "NotchShape", value)

    @property
    @exception_bridge
    def notch_width_lower(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NotchWidthLower")

        if temp is None:
            return 0.0

        return temp

    @notch_width_lower.setter
    @exception_bridge
    @enforce_parameter_types
    def notch_width_lower(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NotchWidthLower", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def notch_width_upper(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NotchWidthUpper")

        if temp is None:
            return 0.0

        return temp

    @notch_width_upper.setter
    @exception_bridge
    @enforce_parameter_types
    def notch_width_upper(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NotchWidthUpper", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def number_of_notches(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfNotches")

        if temp is None:
            return 0

        return temp

    @number_of_notches.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_notches(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfNotches", int(value) if value is not None else 0
        )

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
    def cast_to(self: "Self") -> "_Cast_NotchSpecification":
        """Cast to another type.

        Returns:
            _Cast_NotchSpecification
        """
        return _Cast_NotchSpecification(self)
