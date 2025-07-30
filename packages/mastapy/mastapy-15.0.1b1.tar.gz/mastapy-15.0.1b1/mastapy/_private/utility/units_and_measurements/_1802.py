"""Unit"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_UNIT = python_net_import("SMT.MastaAPI.Utility.UnitsAndMeasurements", "Unit")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.units_and_measurements import (
        _1794,
        _1795,
        _1796,
        _1800,
        _1801,
        _1803,
    )

    Self = TypeVar("Self", bound="Unit")
    CastSelf = TypeVar("CastSelf", bound="Unit._Cast_Unit")


__docformat__ = "restructuredtext en"
__all__ = ("Unit",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Unit:
    """Special nested class for casting Unit to subclasses."""

    __parent__: "Unit"

    @property
    def degrees_minutes_seconds(self: "CastSelf") -> "_1794.DegreesMinutesSeconds":
        from mastapy._private.utility.units_and_measurements import _1794

        return self.__parent__._cast(_1794.DegreesMinutesSeconds)

    @property
    def enum_unit(self: "CastSelf") -> "_1795.EnumUnit":
        from mastapy._private.utility.units_and_measurements import _1795

        return self.__parent__._cast(_1795.EnumUnit)

    @property
    def inverse_unit(self: "CastSelf") -> "_1796.InverseUnit":
        from mastapy._private.utility.units_and_measurements import _1796

        return self.__parent__._cast(_1796.InverseUnit)

    @property
    def safety_factor_unit(self: "CastSelf") -> "_1800.SafetyFactorUnit":
        from mastapy._private.utility.units_and_measurements import _1800

        return self.__parent__._cast(_1800.SafetyFactorUnit)

    @property
    def time_unit(self: "CastSelf") -> "_1801.TimeUnit":
        from mastapy._private.utility.units_and_measurements import _1801

        return self.__parent__._cast(_1801.TimeUnit)

    @property
    def unit_gradient(self: "CastSelf") -> "_1803.UnitGradient":
        from mastapy._private.utility.units_and_measurements import _1803

        return self.__parent__._cast(_1803.UnitGradient)

    @property
    def unit(self: "CastSelf") -> "Unit":
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
class Unit(_0.APIBase):
    """Unit

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _UNIT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def html_symbol(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HTMLSymbol")

        if temp is None:
            return ""

        return temp

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
    def offset(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scale(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Scale")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def symbol(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Symbol")

        if temp is None:
            return ""

        return temp

    @exception_bridge
    @enforce_parameter_types
    def convert_from_si_unit(self: "Self", d: "float") -> "float":
        """float

        Args:
            d (float)
        """
        d = float(d)
        method_result = pythonnet_method_call(
            self.wrapped, "ConvertFromSIUnit", d if d else 0.0
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def convert_to_si_unit(self: "Self", d: "float") -> "float":
        """float

        Args:
            d (float)
        """
        d = float(d)
        method_result = pythonnet_method_call(
            self.wrapped, "ConvertToSIUnit", d if d else 0.0
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_Unit":
        """Cast to another type.

        Returns:
            _Cast_Unit
        """
        return _Cast_Unit(self)
