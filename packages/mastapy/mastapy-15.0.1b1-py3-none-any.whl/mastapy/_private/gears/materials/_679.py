"""BevelGearMaterial"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.materials import _688

_BEVEL_GEAR_MATERIAL = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "BevelGearMaterial"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.materials import _677, _711
    from mastapy._private.materials import _358
    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="BevelGearMaterial")
    CastSelf = TypeVar("CastSelf", bound="BevelGearMaterial._Cast_BevelGearMaterial")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMaterial:
    """Special nested class for casting BevelGearMaterial to subclasses."""

    __parent__: "BevelGearMaterial"

    @property
    def gear_material(self: "CastSelf") -> "_688.GearMaterial":
        return self.__parent__._cast(_688.GearMaterial)

    @property
    def material(self: "CastSelf") -> "_358.Material":
        from mastapy._private.materials import _358

        return self.__parent__._cast(_358.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def bevel_gear_iso_material(self: "CastSelf") -> "_677.BevelGearISOMaterial":
        from mastapy._private.gears.materials import _677

        return self.__parent__._cast(_677.BevelGearISOMaterial)

    @property
    def bevel_gear_material(self: "CastSelf") -> "BevelGearMaterial":
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
class BevelGearMaterial(_688.GearMaterial):
    """BevelGearMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_bending_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AllowableBendingStress")

        if temp is None:
            return 0.0

        return temp

    @allowable_bending_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def allowable_bending_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowableBendingStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def allowable_contact_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AllowableContactStress")

        if temp is None:
            return 0.0

        return temp

    @allowable_contact_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def allowable_contact_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowableContactStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def sn_curve_definition(self: "Self") -> "_711.SNCurveDefinition":
        """mastapy.gears.materials.SNCurveDefinition"""
        temp = pythonnet_property_get(self.wrapped, "SNCurveDefinition")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Materials.SNCurveDefinition"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.materials._711", "SNCurveDefinition"
        )(value)

    @sn_curve_definition.setter
    @exception_bridge
    @enforce_parameter_types
    def sn_curve_definition(self: "Self", value: "_711.SNCurveDefinition") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Materials.SNCurveDefinition"
        )
        pythonnet_property_set(self.wrapped, "SNCurveDefinition", value)

    @property
    @exception_bridge
    def thermal_constant(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalConstant")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearMaterial":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMaterial
        """
        return _Cast_BevelGearMaterial(self)
