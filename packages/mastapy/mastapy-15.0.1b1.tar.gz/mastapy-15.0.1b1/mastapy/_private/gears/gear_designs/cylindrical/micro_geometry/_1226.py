"""GearAlignment"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEAR_ALIGNMENT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry", "GearAlignment"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1135

    Self = TypeVar("Self", bound="GearAlignment")
    CastSelf = TypeVar("CastSelf", bound="GearAlignment._Cast_GearAlignment")


__docformat__ = "restructuredtext en"
__all__ = ("GearAlignment",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearAlignment:
    """Special nested class for casting GearAlignment to subclasses."""

    __parent__: "GearAlignment"

    @property
    def gear_alignment(self: "CastSelf") -> "GearAlignment":
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
class GearAlignment(_0.APIBase):
    """GearAlignment

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_ALIGNMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def index_of_reference_tooth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "IndexOfReferenceTooth")

        if temp is None:
            return 0

        return temp

    @index_of_reference_tooth.setter
    @exception_bridge
    @enforce_parameter_types
    def index_of_reference_tooth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IndexOfReferenceTooth",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Radius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def roll_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RollDistance")

        if temp is None:
            return 0.0

        return temp

    @roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def roll_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RollDistance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def profile_measurement_of_the_tooth_at_least_roll_distance(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileMeasurementOfTheToothAtLeastRollDistance"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearAlignment":
        """Cast to another type.

        Returns:
            _Cast_GearAlignment
        """
        return _Cast_GearAlignment(self)
