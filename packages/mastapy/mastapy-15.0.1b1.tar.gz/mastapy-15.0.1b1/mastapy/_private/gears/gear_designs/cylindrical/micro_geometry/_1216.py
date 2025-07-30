"""CylindricalGearMicroGeometryMap"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_CYLINDRICAL_GEAR_MICRO_GEOMETRY_MAP = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearMicroGeometryMap",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1135
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1233

    Self = TypeVar("Self", bound="CylindricalGearMicroGeometryMap")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMicroGeometryMap._Cast_CylindricalGearMicroGeometryMap",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMicroGeometryMap",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMicroGeometryMap:
    """Special nested class for casting CylindricalGearMicroGeometryMap to subclasses."""

    __parent__: "CylindricalGearMicroGeometryMap"

    @property
    def cylindrical_gear_micro_geometry_map(
        self: "CastSelf",
    ) -> "CylindricalGearMicroGeometryMap":
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
class CylindricalGearMicroGeometryMap(_0.APIBase):
    """CylindricalGearMicroGeometryMap

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MICRO_GEOMETRY_MAP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def measured_map_data_type(self: "Self") -> "_1233.MeasuredMapDataTypes":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.MeasuredMapDataTypes"""
        temp = pythonnet_property_get(self.wrapped, "MeasuredMapDataType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry.MeasuredMapDataTypes",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1233",
            "MeasuredMapDataTypes",
        )(value)

    @measured_map_data_type.setter
    @exception_bridge
    @enforce_parameter_types
    def measured_map_data_type(
        self: "Self", value: "_1233.MeasuredMapDataTypes"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry.MeasuredMapDataTypes",
        )
        pythonnet_property_set(self.wrapped, "MeasuredMapDataType", value)

    @property
    @exception_bridge
    def profile_factor_for_0_bias_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileFactorFor0BiasRelief")

        if temp is None:
            return 0.0

        return temp

    @profile_factor_for_0_bias_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_factor_for_0_bias_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileFactorFor0BiasRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def zero_bias_relief(self: "Self") -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZeroBiasRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMicroGeometryMap":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMicroGeometryMap
        """
        return _Cast_CylindricalGearMicroGeometryMap(self)
