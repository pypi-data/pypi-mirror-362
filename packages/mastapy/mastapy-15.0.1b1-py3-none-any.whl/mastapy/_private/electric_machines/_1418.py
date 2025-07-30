"""MagnetMaterial"""

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
from mastapy._private.materials import _358

_MAGNET_MATERIAL = python_net_import("SMT.MastaAPI.ElectricMachines", "MagnetMaterial")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="MagnetMaterial")
    CastSelf = TypeVar("CastSelf", bound="MagnetMaterial._Cast_MagnetMaterial")


__docformat__ = "restructuredtext en"
__all__ = ("MagnetMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MagnetMaterial:
    """Special nested class for casting MagnetMaterial to subclasses."""

    __parent__: "MagnetMaterial"

    @property
    def material(self: "CastSelf") -> "_358.Material":
        return self.__parent__._cast(_358.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def magnet_material(self: "CastSelf") -> "MagnetMaterial":
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
class MagnetMaterial(_358.Material):
    """MagnetMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MAGNET_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def country(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Country")

        if temp is None:
            return ""

        return temp

    @country.setter
    @exception_bridge
    @enforce_parameter_types
    def country(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Country", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def electrical_resistivity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ElectricalResistivity")

        if temp is None:
            return 0.0

        return temp

    @electrical_resistivity.setter
    @exception_bridge
    @enforce_parameter_types
    def electrical_resistivity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ElectricalResistivity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def grade(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Grade")

        if temp is None:
            return ""

        return temp

    @grade.setter
    @exception_bridge
    @enforce_parameter_types
    def grade(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Grade", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def manufacturer(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Manufacturer")

        if temp is None:
            return ""

        return temp

    @manufacturer.setter
    @exception_bridge
    @enforce_parameter_types
    def manufacturer(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Manufacturer", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def material_category(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "MaterialCategory")

        if temp is None:
            return ""

        return temp

    @material_category.setter
    @exception_bridge
    @enforce_parameter_types
    def material_category(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "MaterialCategory", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def relative_permeability(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RelativePermeability")

        if temp is None:
            return 0.0

        return temp

    @relative_permeability.setter
    @exception_bridge
    @enforce_parameter_types
    def relative_permeability(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RelativePermeability",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def remanence_at_20_degrees_c(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RemanenceAt20DegreesC")

        if temp is None:
            return 0.0

        return temp

    @remanence_at_20_degrees_c.setter
    @exception_bridge
    @enforce_parameter_types
    def remanence_at_20_degrees_c(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RemanenceAt20DegreesC",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def temperature_coefficient_for_remanence(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TemperatureCoefficientForRemanence"
        )

        if temp is None:
            return 0.0

        return temp

    @temperature_coefficient_for_remanence.setter
    @exception_bridge
    @enforce_parameter_types
    def temperature_coefficient_for_remanence(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TemperatureCoefficientForRemanence",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MagnetMaterial":
        """Cast to another type.

        Returns:
            _Cast_MagnetMaterial
        """
        return _Cast_MagnetMaterial(self)
