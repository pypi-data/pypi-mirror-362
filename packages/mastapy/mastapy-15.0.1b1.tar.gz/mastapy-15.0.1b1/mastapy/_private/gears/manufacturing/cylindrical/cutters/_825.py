"""RoughCutterCreationSettings"""

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

_ROUGH_CUTTER_CREATION_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters",
    "RoughCutterCreationSettings",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1195
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _844

    Self = TypeVar("Self", bound="RoughCutterCreationSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RoughCutterCreationSettings._Cast_RoughCutterCreationSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RoughCutterCreationSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RoughCutterCreationSettings:
    """Special nested class for casting RoughCutterCreationSettings to subclasses."""

    __parent__: "RoughCutterCreationSettings"

    @property
    def rough_cutter_creation_settings(
        self: "CastSelf",
    ) -> "RoughCutterCreationSettings":
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
class RoughCutterCreationSettings(_0.APIBase):
    """RoughCutterCreationSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROUGH_CUTTER_CREATION_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def finish_thickness_used_to_generate_cutter(
        self: "Self",
    ) -> "_1195.TolerancedMetalMeasurements":
        """mastapy.gears.gear_designs.cylindrical.TolerancedMetalMeasurements"""
        temp = pythonnet_property_get(
            self.wrapped, "FinishThicknessUsedToGenerateCutter"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.TolerancedMetalMeasurements",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1195",
            "TolerancedMetalMeasurements",
        )(value)

    @finish_thickness_used_to_generate_cutter.setter
    @exception_bridge
    @enforce_parameter_types
    def finish_thickness_used_to_generate_cutter(
        self: "Self", value: "_1195.TolerancedMetalMeasurements"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.TolerancedMetalMeasurements",
        )
        pythonnet_property_set(
            self.wrapped, "FinishThicknessUsedToGenerateCutter", value
        )

    @property
    @exception_bridge
    def rough_thickness_used_to_generate_cutter(
        self: "Self",
    ) -> "_1195.TolerancedMetalMeasurements":
        """mastapy.gears.gear_designs.cylindrical.TolerancedMetalMeasurements"""
        temp = pythonnet_property_get(
            self.wrapped, "RoughThicknessUsedToGenerateCutter"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.TolerancedMetalMeasurements",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1195",
            "TolerancedMetalMeasurements",
        )(value)

    @rough_thickness_used_to_generate_cutter.setter
    @exception_bridge
    @enforce_parameter_types
    def rough_thickness_used_to_generate_cutter(
        self: "Self", value: "_1195.TolerancedMetalMeasurements"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.TolerancedMetalMeasurements",
        )
        pythonnet_property_set(
            self.wrapped, "RoughThicknessUsedToGenerateCutter", value
        )

    @property
    @exception_bridge
    def finish_tool_clearances(
        self: "Self",
    ) -> "_844.ManufacturingOperationConstraints":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.ManufacturingOperationConstraints

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinishToolClearances")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rough_tool_clearances(self: "Self") -> "_844.ManufacturingOperationConstraints":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.ManufacturingOperationConstraints

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughToolClearances")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RoughCutterCreationSettings":
        """Cast to another type.

        Returns:
            _Cast_RoughCutterCreationSettings
        """
        return _Cast_RoughCutterCreationSettings(self)
