"""LengthShort"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.utility.units_and_measurements import _1797

_LENGTH_SHORT = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements", "LengthShort"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.units_and_measurements import _1802

    Self = TypeVar("Self", bound="LengthShort")
    CastSelf = TypeVar("CastSelf", bound="LengthShort._Cast_LengthShort")


__docformat__ = "restructuredtext en"
__all__ = ("LengthShort",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LengthShort:
    """Special nested class for casting LengthShort to subclasses."""

    __parent__: "LengthShort"

    @property
    def measurement_base(self: "CastSelf") -> "_1797.MeasurementBase":
        return self.__parent__._cast(_1797.MeasurementBase)

    @property
    def length_short(self: "CastSelf") -> "LengthShort":
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
class LengthShort(_1797.MeasurementBase):
    """LengthShort

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LENGTH_SHORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def feet(self: "Self") -> "_1802.Unit":
        """mastapy.utility.units_and_measurements.Unit

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Feet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inches(self: "Self") -> "_1802.Unit":
        """mastapy.utility.units_and_measurements.Unit

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Inches")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def metres(self: "Self") -> "_1802.Unit":
        """mastapy.utility.units_and_measurements.Unit

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Metres")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micrometres(self: "Self") -> "_1802.Unit":
        """mastapy.utility.units_and_measurements.Unit

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Micrometres")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def millimetres(self: "Self") -> "_1802.Unit":
        """mastapy.utility.units_and_measurements.Unit

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Millimetres")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def thousandths_of_an_inch(self: "Self") -> "_1802.Unit":
        """mastapy.utility.units_and_measurements.Unit

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThousandthsOfAnInch")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LengthShort":
        """Cast to another type.

        Returns:
            _Cast_LengthShort
        """
        return _Cast_LengthShort(self)
