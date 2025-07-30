"""LoadedBearingTemperatureChart"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.utility.report import _1951

_LOADED_BEARING_TEMPERATURE_CHART = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedBearingTemperatureChart"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1958, _1964, _1965, _1966

    Self = TypeVar("Self", bound="LoadedBearingTemperatureChart")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedBearingTemperatureChart._Cast_LoadedBearingTemperatureChart",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedBearingTemperatureChart",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedBearingTemperatureChart:
    """Special nested class for casting LoadedBearingTemperatureChart to subclasses."""

    __parent__: "LoadedBearingTemperatureChart"

    @property
    def custom_report_chart(self: "CastSelf") -> "_1951.CustomReportChart":
        return self.__parent__._cast(_1951.CustomReportChart)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1964.CustomReportMultiPropertyItem":
        pass

        from mastapy._private.utility.report import _1964

        return self.__parent__._cast(_1964.CustomReportMultiPropertyItem)

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1965.CustomReportMultiPropertyItemBase":
        from mastapy._private.utility.report import _1965

        return self.__parent__._cast(_1965.CustomReportMultiPropertyItemBase)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1966.CustomReportNameableItem":
        from mastapy._private.utility.report import _1966

        return self.__parent__._cast(_1966.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def loaded_bearing_temperature_chart(
        self: "CastSelf",
    ) -> "LoadedBearingTemperatureChart":
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
class LoadedBearingTemperatureChart(_1951.CustomReportChart):
    """LoadedBearingTemperatureChart

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_BEARING_TEMPERATURE_CHART

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumTemperature")

        if temp is None:
            return 0.0

        return temp

    @maximum_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumTemperature")

        if temp is None:
            return 0.0

        return temp

    @minimum_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_steps(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfSteps")

        if temp is None:
            return 0

        return temp

    @number_of_steps.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_steps(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfSteps", int(value) if value is not None else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedBearingTemperatureChart":
        """Cast to another type.

        Returns:
            _Cast_LoadedBearingTemperatureChart
        """
        return _Cast_LoadedBearingTemperatureChart(self)
