"""RingPinsDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
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

_RING_PINS_DESIGN = python_net_import("SMT.MastaAPI.Cycloidal", "RingPinsDesign")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="RingPinsDesign")
    CastSelf = TypeVar("CastSelf", bound="RingPinsDesign._Cast_RingPinsDesign")


__docformat__ = "restructuredtext en"
__all__ = ("RingPinsDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingPinsDesign:
    """Special nested class for casting RingPinsDesign to subclasses."""

    __parent__: "RingPinsDesign"

    @property
    def ring_pins_design(self: "CastSelf") -> "RingPinsDesign":
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
class RingPinsDesign(_0.APIBase):
    """RingPinsDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_PINS_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def length_of_pins(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LengthOfPins")

        if temp is None:
            return 0.0

        return temp

    @length_of_pins.setter
    @exception_bridge
    @enforce_parameter_types
    def length_of_pins(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LengthOfPins", float(value) if value is not None else 0.0
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
    def number_of_pins(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPins")

        if temp is None:
            return 0

        return temp

    @number_of_pins.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_pins(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfPins", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def pin_centre_circle_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinCentreCircleDiameter")

        if temp is None:
            return 0.0

        return temp

    @pin_centre_circle_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def pin_centre_circle_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinCentreCircleDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pin_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinDiameter")

        if temp is None:
            return 0.0

        return temp

    @pin_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def pin_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PinDiameter", float(value) if value is not None else 0.0
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
    def cast_to(self: "Self") -> "_Cast_RingPinsDesign":
        """Cast to another type.

        Returns:
            _Cast_RingPinsDesign
        """
        return _Cast_RingPinsDesign(self)
