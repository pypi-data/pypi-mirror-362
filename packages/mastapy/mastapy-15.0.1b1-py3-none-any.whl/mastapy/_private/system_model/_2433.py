"""SystemReporting"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_SYSTEM_REPORTING = python_net_import("SMT.MastaAPI.SystemModel", "SystemReporting")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.utility.units_and_measurements import _1797

    Self = TypeVar("Self", bound="SystemReporting")
    CastSelf = TypeVar("CastSelf", bound="SystemReporting._Cast_SystemReporting")


__docformat__ = "restructuredtext en"
__all__ = ("SystemReporting",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SystemReporting:
    """Special nested class for casting SystemReporting to subclasses."""

    __parent__: "SystemReporting"

    @property
    def system_reporting(self: "CastSelf") -> "SystemReporting":
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
class SystemReporting(_0.APIBase):
    """SystemReporting

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYSTEM_REPORTING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def current_date_and_time(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentDateAndTime")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def current_date_and_time_iso8601(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentDateAndTimeISO8601")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def masta_version(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MASTAVersion")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def all_measurements(self: "Self") -> "List[_1797.MeasurementBase]":
        """List[mastapy.utility.units_and_measurements.MeasurementBase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllMeasurements")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def measurements_not_using_si_unit(self: "Self") -> "List[_1797.MeasurementBase]":
        """List[mastapy.utility.units_and_measurements.MeasurementBase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeasurementsNotUsingSIUnit")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SystemReporting":
        """Cast to another type.

        Returns:
            _Cast_SystemReporting
        """
        return _Cast_SystemReporting(self)
