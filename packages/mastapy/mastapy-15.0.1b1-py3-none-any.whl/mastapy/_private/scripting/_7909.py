"""MastaPropertyAttribute"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_MASTA_PROPERTY_ATTRIBUTE = python_net_import(
    "SMT.MastaAPIUtility.Scripting", "MastaPropertyAttribute"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.units_and_measurements import _7903

    Self = TypeVar("Self", bound="MastaPropertyAttribute")
    CastSelf = TypeVar(
        "CastSelf", bound="MastaPropertyAttribute._Cast_MastaPropertyAttribute"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MastaPropertyAttribute",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MastaPropertyAttribute:
    """Special nested class for casting MastaPropertyAttribute to subclasses."""

    __parent__: "MastaPropertyAttribute"

    @property
    def masta_property_attribute(self: "CastSelf") -> "MastaPropertyAttribute":
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
class MastaPropertyAttribute:
    """MastaPropertyAttribute

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MASTA_PROPERTY_ATTRIBUTE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def description(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Description")

        if temp is None:
            return ""

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

    @property
    @exception_bridge
    def measurement(self: "Self") -> "_7903.MeasurementType":
        """mastapy.units_and_measurements.MeasurementType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Measurement")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPIUtility.UnitsAndMeasurements.MeasurementType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.units_and_measurements._7903", "MeasurementType"
        )(value)

    @property
    def cast_to(self: "Self") -> "_Cast_MastaPropertyAttribute":
        """Cast to another type.

        Returns:
            _Cast_MastaPropertyAttribute
        """
        return _Cast_MastaPropertyAttribute(self)
