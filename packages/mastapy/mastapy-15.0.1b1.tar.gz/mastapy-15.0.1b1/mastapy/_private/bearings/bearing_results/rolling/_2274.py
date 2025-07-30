"""PreloadFactorLookupTable"""

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

_PRELOAD_FACTOR_LOOKUP_TABLE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "PreloadFactorLookupTable"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="PreloadFactorLookupTable")
    CastSelf = TypeVar(
        "CastSelf", bound="PreloadFactorLookupTable._Cast_PreloadFactorLookupTable"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PreloadFactorLookupTable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PreloadFactorLookupTable:
    """Special nested class for casting PreloadFactorLookupTable to subclasses."""

    __parent__: "PreloadFactorLookupTable"

    @property
    def preload_factor_lookup_table(self: "CastSelf") -> "PreloadFactorLookupTable":
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
class PreloadFactorLookupTable(_0.APIBase):
    """PreloadFactorLookupTable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PRELOAD_FACTOR_LOOKUP_TABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def high(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "High")

        if temp is None:
            return 0.0

        return temp

    @high.setter
    @exception_bridge
    @enforce_parameter_types
    def high(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "High", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def low(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Low")

        if temp is None:
            return 0.0

        return temp

    @low.setter
    @exception_bridge
    @enforce_parameter_types
    def low(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Low", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def medium(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Medium")

        if temp is None:
            return 0.0

        return temp

    @medium.setter
    @exception_bridge
    @enforce_parameter_types
    def medium(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Medium", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def zero(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Zero")

        if temp is None:
            return 0.0

        return temp

    @zero.setter
    @exception_bridge
    @enforce_parameter_types
    def zero(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Zero", float(value) if value is not None else 0.0
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
    def cast_to(self: "Self") -> "_Cast_PreloadFactorLookupTable":
        """Cast to another type.

        Returns:
            _Cast_PreloadFactorLookupTable
        """
        return _Cast_PreloadFactorLookupTable(self)
