"""PinionRoughMachineSetting"""

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

_PINION_ROUGH_MACHINE_SETTING = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "PinionRoughMachineSetting"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1276
    from mastapy._private.gears.manufacturing.bevel import _891

    Self = TypeVar("Self", bound="PinionRoughMachineSetting")
    CastSelf = TypeVar(
        "CastSelf", bound="PinionRoughMachineSetting._Cast_PinionRoughMachineSetting"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PinionRoughMachineSetting",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PinionRoughMachineSetting:
    """Special nested class for casting PinionRoughMachineSetting to subclasses."""

    __parent__: "PinionRoughMachineSetting"

    @property
    def pinion_rough_machine_setting(self: "CastSelf") -> "PinionRoughMachineSetting":
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
class PinionRoughMachineSetting(_0.APIBase):
    """PinionRoughMachineSetting

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PINION_ROUGH_MACHINE_SETTING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def absolute_increment_in_machine_centre_to_back(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AbsoluteIncrementInMachineCentreToBack"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def blank_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BlankOffset")

        if temp is None:
            return 0.0

        return temp

    @blank_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def blank_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BlankOffset", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def cone_distance_of_reference_point(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ConeDistanceOfReferencePoint")

        if temp is None:
            return 0.0

        return temp

    @cone_distance_of_reference_point.setter
    @exception_bridge
    @enforce_parameter_types
    def cone_distance_of_reference_point(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ConeDistanceOfReferencePoint",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def height_of_reference_point(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HeightOfReferencePoint")

        if temp is None:
            return 0.0

        return temp

    @height_of_reference_point.setter
    @exception_bridge
    @enforce_parameter_types
    def height_of_reference_point(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HeightOfReferencePoint",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def increment_of_pinion_workpiece_mounting_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "IncrementOfPinionWorkpieceMountingDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @increment_of_pinion_workpiece_mounting_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def increment_of_pinion_workpiece_mounting_distance(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncrementOfPinionWorkpieceMountingDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_allowed_finish_stock(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumAllowedFinishStock")

        if temp is None:
            return 0.0

        return temp

    @minimum_allowed_finish_stock.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_allowed_finish_stock(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumAllowedFinishStock",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def spiral_angle_at_reference_point(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpiralAngleAtReferencePoint")

        if temp is None:
            return 0.0

        return temp

    @spiral_angle_at_reference_point.setter
    @exception_bridge
    @enforce_parameter_types
    def spiral_angle_at_reference_point(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpiralAngleAtReferencePoint",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def gear_set(self: "Self") -> "_1276.ConicalGearSetDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pinion_config(self: "Self") -> "_891.ConicalPinionManufacturingConfig":
        """mastapy.gears.manufacturing.bevel.ConicalPinionManufacturingConfig

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionConfig")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PinionRoughMachineSetting":
        """Cast to another type.

        Returns:
            _Cast_PinionRoughMachineSetting
        """
        return _Cast_PinionRoughMachineSetting(self)
