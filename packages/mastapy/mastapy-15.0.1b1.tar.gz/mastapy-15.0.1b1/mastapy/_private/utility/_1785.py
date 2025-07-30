"""NumberFormatInfoSummary"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_NUMBER_FORMAT_INFO_SUMMARY = python_net_import(
    "SMT.MastaAPI.Utility", "NumberFormatInfoSummary"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NumberFormatInfoSummary")
    CastSelf = TypeVar(
        "CastSelf", bound="NumberFormatInfoSummary._Cast_NumberFormatInfoSummary"
    )


__docformat__ = "restructuredtext en"
__all__ = ("NumberFormatInfoSummary",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NumberFormatInfoSummary:
    """Special nested class for casting NumberFormatInfoSummary to subclasses."""

    __parent__: "NumberFormatInfoSummary"

    @property
    def number_format_info_summary(self: "CastSelf") -> "NumberFormatInfoSummary":
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
class NumberFormatInfoSummary(_0.APIBase):
    """NumberFormatInfoSummary

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NUMBER_FORMAT_INFO_SUMMARY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def decimal_symbol(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DecimalSymbol")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def native_digits(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NativeDigits")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def negative_pattern(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NegativePattern")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def negative_symbol(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NegativeSymbol")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def sample_negative_number(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SampleNegativeNumber")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def sample_positive_number(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SamplePositiveNumber")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_NumberFormatInfoSummary":
        """Cast to another type.

        Returns:
            _Cast_NumberFormatInfoSummary
        """
        return _Cast_NumberFormatInfoSummary(self)
