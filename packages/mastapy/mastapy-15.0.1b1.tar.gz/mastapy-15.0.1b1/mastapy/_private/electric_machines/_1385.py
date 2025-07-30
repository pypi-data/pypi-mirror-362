"""Eccentricity"""

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
from mastapy._private.utility import _1779

_ECCENTRICITY = python_net_import("SMT.MastaAPI.ElectricMachines", "Eccentricity")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Eccentricity")
    CastSelf = TypeVar("CastSelf", bound="Eccentricity._Cast_Eccentricity")


__docformat__ = "restructuredtext en"
__all__ = ("Eccentricity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Eccentricity:
    """Special nested class for casting Eccentricity to subclasses."""

    __parent__: "Eccentricity"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def eccentricity(self: "CastSelf") -> "Eccentricity":
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
class Eccentricity(_1779.IndependentReportablePropertiesBase["Eccentricity"]):
    """Eccentricity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ECCENTRICITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def dynamic_x(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DynamicX")

        if temp is None:
            return 0.0

        return temp

    @dynamic_x.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_x(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DynamicX", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def dynamic_y(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DynamicY")

        if temp is None:
            return 0.0

        return temp

    @dynamic_y.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_y(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DynamicY", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def static_x(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StaticX")

        if temp is None:
            return 0.0

        return temp

    @static_x.setter
    @exception_bridge
    @enforce_parameter_types
    def static_x(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StaticX", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def static_y(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StaticY")

        if temp is None:
            return 0.0

        return temp

    @static_y.setter
    @exception_bridge
    @enforce_parameter_types
    def static_y(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StaticY", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Eccentricity":
        """Cast to another type.

        Returns:
            _Cast_Eccentricity
        """
        return _Cast_Eccentricity(self)
