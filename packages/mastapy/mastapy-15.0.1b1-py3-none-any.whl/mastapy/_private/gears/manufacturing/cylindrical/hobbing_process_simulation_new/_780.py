"""HobResharpeningError"""

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

_HOB_RESHARPENING_ERROR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "HobResharpeningError",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="HobResharpeningError")
    CastSelf = TypeVar(
        "CastSelf", bound="HobResharpeningError._Cast_HobResharpeningError"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HobResharpeningError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HobResharpeningError:
    """Special nested class for casting HobResharpeningError to subclasses."""

    __parent__: "HobResharpeningError"

    @property
    def hob_resharpening_error(self: "CastSelf") -> "HobResharpeningError":
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
class HobResharpeningError(_0.APIBase):
    """HobResharpeningError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HOB_RESHARPENING_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gash_lead_error_reading(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GashLeadErrorReading")

        if temp is None:
            return 0.0

        return temp

    @gash_lead_error_reading.setter
    @exception_bridge
    @enforce_parameter_types
    def gash_lead_error_reading(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GashLeadErrorReading",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def gash_lead_measurement_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GashLeadMeasurementLength")

        if temp is None:
            return 0.0

        return temp

    @gash_lead_measurement_length.setter
    @exception_bridge
    @enforce_parameter_types
    def gash_lead_measurement_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GashLeadMeasurementLength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def radial_alignment_error_reading(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialAlignmentErrorReading")

        if temp is None:
            return 0.0

        return temp

    @radial_alignment_error_reading.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_alignment_error_reading(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialAlignmentErrorReading",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def radial_alignment_measurement_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialAlignmentMeasurementLength")

        if temp is None:
            return 0.0

        return temp

    @radial_alignment_measurement_length.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_alignment_measurement_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialAlignmentMeasurementLength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def total_gash_indexing_variation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TotalGashIndexingVariation")

        if temp is None:
            return 0.0

        return temp

    @total_gash_indexing_variation.setter
    @exception_bridge
    @enforce_parameter_types
    def total_gash_indexing_variation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TotalGashIndexingVariation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_sin_curve_for_gash_index_variation(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSinCurveForGashIndexVariation")

        if temp is None:
            return False

        return temp

    @use_sin_curve_for_gash_index_variation.setter
    @exception_bridge
    @enforce_parameter_types
    def use_sin_curve_for_gash_index_variation(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSinCurveForGashIndexVariation",
            bool(value) if value is not None else False,
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
    def cast_to(self: "Self") -> "_Cast_HobResharpeningError":
        """Cast to another type.

        Returns:
            _Cast_HobResharpeningError
        """
        return _Cast_HobResharpeningError(self)
