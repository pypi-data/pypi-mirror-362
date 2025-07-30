"""TimeOptions"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_TIME_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "TimeOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TimeOptions")
    CastSelf = TypeVar("CastSelf", bound="TimeOptions._Cast_TimeOptions")


__docformat__ = "restructuredtext en"
__all__ = ("TimeOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TimeOptions:
    """Special nested class for casting TimeOptions to subclasses."""

    __parent__: "TimeOptions"

    @property
    def time_options(self: "CastSelf") -> "TimeOptions":
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
class TimeOptions(_0.APIBase):
    """TimeOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TIME_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def end_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EndTime")

        if temp is None:
            return 0.0

        return temp

    @end_time.setter
    @exception_bridge
    @enforce_parameter_types
    def end_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EndTime", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def start_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartTime")

        if temp is None:
            return 0.0

        return temp

    @start_time.setter
    @exception_bridge
    @enforce_parameter_types
    def start_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StartTime", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def total_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TotalTime")

        if temp is None:
            return 0.0

        return temp

    @total_time.setter
    @exception_bridge
    @enforce_parameter_types
    def total_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TotalTime", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TimeOptions":
        """Cast to another type.

        Returns:
            _Cast_TimeOptions
        """
        return _Cast_TimeOptions(self)
