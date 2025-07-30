"""DataLogger"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D

_DATA_LOGGER = python_net_import("SMT.MastaAPI.MathUtility.Convergence", "DataLogger")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility.convergence import _1759
    from mastapy._private.utility_gui import _2053

    Self = TypeVar("Self", bound="DataLogger")
    CastSelf = TypeVar("CastSelf", bound="DataLogger._Cast_DataLogger")


__docformat__ = "restructuredtext en"
__all__ = ("DataLogger",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DataLogger:
    """Special nested class for casting DataLogger to subclasses."""

    __parent__: "DataLogger"

    @property
    def convergence_logger(self: "CastSelf") -> "_1759.ConvergenceLogger":
        from mastapy._private.math_utility.convergence import _1759

        return self.__parent__._cast(_1759.ConvergenceLogger)

    @property
    def data_logger_with_charts(self: "CastSelf") -> "_2053.DataLoggerWithCharts":
        from mastapy._private.utility_gui import _2053

        return self.__parent__._cast(_2053.DataLoggerWithCharts)

    @property
    def data_logger(self: "CastSelf") -> "DataLogger":
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
class DataLogger(_0.APIBase):
    """DataLogger

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATA_LOGGER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def available_properties(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AvailableProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def has_logged_data(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasLoggedData")

        if temp is None:
            return False

        return temp

    @exception_bridge
    @enforce_parameter_types
    def get_double_data_for(self: "Self", property_name: "str") -> "List[float]":
        """List[float]

        Args:
            property_name (str)
        """
        property_name = str(property_name)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "GetDoubleDataFor", property_name if property_name else ""
            ),
            float,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_int_data_for(self: "Self", property_name: "str") -> "List[int]":
        """List[int]

        Args:
            property_name (str)
        """
        property_name = str(property_name)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "GetIntDataFor", property_name if property_name else ""
            ),
            int,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_vector_data_for(self: "Self", property_name: "str") -> "List[Vector3D]":
        """List[Vector3D]

        Args:
            property_name (str)
        """
        property_name = str(property_name)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "GetVectorDataFor", property_name if property_name else ""
            ),
            Vector3D,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_DataLogger":
        """Cast to another type.

        Returns:
            _Cast_DataLogger
        """
        return _Cast_DataLogger(self)
