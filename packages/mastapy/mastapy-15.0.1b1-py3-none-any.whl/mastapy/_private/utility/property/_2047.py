"""NamedRangeWithOverridableMinAndMax"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_NAMED_RANGE_WITH_OVERRIDABLE_MIN_AND_MAX = python_net_import(
    "SMT.MastaAPI.Utility.Property", "NamedRangeWithOverridableMinAndMax"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.utility.units_and_measurements import _1797

    Self = TypeVar("Self", bound="NamedRangeWithOverridableMinAndMax")
    CastSelf = TypeVar(
        "CastSelf",
        bound="NamedRangeWithOverridableMinAndMax._Cast_NamedRangeWithOverridableMinAndMax",
    )

T = TypeVar("T")
TMeasurement = TypeVar("TMeasurement", bound="_1797.MeasurementBase")

__docformat__ = "restructuredtext en"
__all__ = ("NamedRangeWithOverridableMinAndMax",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NamedRangeWithOverridableMinAndMax:
    """Special nested class for casting NamedRangeWithOverridableMinAndMax to subclasses."""

    __parent__: "NamedRangeWithOverridableMinAndMax"

    @property
    def named_range_with_overridable_min_and_max(
        self: "CastSelf",
    ) -> "NamedRangeWithOverridableMinAndMax":
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
class NamedRangeWithOverridableMinAndMax(_0.APIBase, Generic[T, TMeasurement]):
    """NamedRangeWithOverridableMinAndMax

    This is a mastapy class.

    Generic Types:
        T
        TMeasurement
    """

    TYPE: ClassVar["Type"] = _NAMED_RANGE_WITH_OVERRIDABLE_MIN_AND_MAX

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def max(self: "Self") -> "overridable.Overridable_T":
        """Overridable[T]"""
        temp = pythonnet_property_get(self.wrapped, "Max")

        if temp is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_T"
        )(temp)

    @max.setter
    @exception_bridge
    @enforce_parameter_types
    def max(self: "Self", value: "Union[T, Tuple[T, bool]]") -> None:
        wrapper_type = overridable.Overridable_T.wrapper_type()
        enclosed_type = overridable.Overridable_T.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Max", value)

    @property
    @exception_bridge
    def min(self: "Self") -> "overridable.Overridable_T":
        """Overridable[T]"""
        temp = pythonnet_property_get(self.wrapped, "Min")

        if temp is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_T"
        )(temp)

    @min.setter
    @exception_bridge
    @enforce_parameter_types
    def min(self: "Self", value: "Union[T, Tuple[T, bool]]") -> None:
        wrapper_type = overridable.Overridable_T.wrapper_type()
        enclosed_type = overridable.Overridable_T.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Min", value)

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
    def cast_to(self: "Self") -> "_Cast_NamedRangeWithOverridableMinAndMax":
        """Cast to another type.

        Returns:
            _Cast_NamedRangeWithOverridableMinAndMax
        """
        return _Cast_NamedRangeWithOverridableMinAndMax(self)
