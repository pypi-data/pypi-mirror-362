"""DataLoggerWithCharts"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.math_utility.convergence import _1760

_DATA_LOGGER_WITH_CHARTS = python_net_import(
    "SMT.MastaAPI.UtilityGUI", "DataLoggerWithCharts"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.utility_gui import _2052

    Self = TypeVar("Self", bound="DataLoggerWithCharts")
    CastSelf = TypeVar(
        "CastSelf", bound="DataLoggerWithCharts._Cast_DataLoggerWithCharts"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DataLoggerWithCharts",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DataLoggerWithCharts:
    """Special nested class for casting DataLoggerWithCharts to subclasses."""

    __parent__: "DataLoggerWithCharts"

    @property
    def data_logger(self: "CastSelf") -> "_1760.DataLogger":
        return self.__parent__._cast(_1760.DataLogger)

    @property
    def data_logger_with_charts(self: "CastSelf") -> "DataLoggerWithCharts":
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
class DataLoggerWithCharts(_1760.DataLogger):
    """DataLoggerWithCharts

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATA_LOGGER_WITH_CHARTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def logged_items(self: "Self") -> "List[_2052.DataLoggerItem]":
        """List[mastapy.utility_gui.DataLoggerItem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoggedItems")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_DataLoggerWithCharts":
        """Cast to another type.

        Returns:
            _Cast_DataLoggerWithCharts
        """
        return _Cast_DataLoggerWithCharts(self)
