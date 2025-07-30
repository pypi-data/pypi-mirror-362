"""BasicConicalGearMachineSettingsGenerated"""

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
from mastapy._private.gears.manufacturing.bevel.basic_machine_settings import _924

_BASIC_CONICAL_GEAR_MACHINE_SETTINGS_GENERATED = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel.BasicMachineSettings",
    "BasicConicalGearMachineSettingsGenerated",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BasicConicalGearMachineSettingsGenerated")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BasicConicalGearMachineSettingsGenerated._Cast_BasicConicalGearMachineSettingsGenerated",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BasicConicalGearMachineSettingsGenerated",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BasicConicalGearMachineSettingsGenerated:
    """Special nested class for casting BasicConicalGearMachineSettingsGenerated to subclasses."""

    __parent__: "BasicConicalGearMachineSettingsGenerated"

    @property
    def basic_conical_gear_machine_settings(
        self: "CastSelf",
    ) -> "_924.BasicConicalGearMachineSettings":
        return self.__parent__._cast(_924.BasicConicalGearMachineSettings)

    @property
    def basic_conical_gear_machine_settings_generated(
        self: "CastSelf",
    ) -> "BasicConicalGearMachineSettingsGenerated":
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
class BasicConicalGearMachineSettingsGenerated(_924.BasicConicalGearMachineSettings):
    """BasicConicalGearMachineSettingsGenerated

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BASIC_CONICAL_GEAR_MACHINE_SETTINGS_GENERATED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def basic_cradle_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BasicCradleAngle")

        if temp is None:
            return 0.0

        return temp

    @basic_cradle_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def basic_cradle_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BasicCradleAngle", float(value) if value is not None else 0.0
        )

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
    def modified_roll_coefficient_c(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ModifiedRollCoefficientC")

        if temp is None:
            return 0.0

        return temp

    @modified_roll_coefficient_c.setter
    @exception_bridge
    @enforce_parameter_types
    def modified_roll_coefficient_c(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModifiedRollCoefficientC",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def modified_roll_coefficient_d(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ModifiedRollCoefficientD")

        if temp is None:
            return 0.0

        return temp

    @modified_roll_coefficient_d.setter
    @exception_bridge
    @enforce_parameter_types
    def modified_roll_coefficient_d(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModifiedRollCoefficientD",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def radial_setting(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialSetting")

        if temp is None:
            return 0.0

        return temp

    @radial_setting.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_setting(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialSetting", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def ratio_of_roll(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RatioOfRoll")

        if temp is None:
            return 0.0

        return temp

    @ratio_of_roll.setter
    @exception_bridge
    @enforce_parameter_types
    def ratio_of_roll(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RatioOfRoll", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BasicConicalGearMachineSettingsGenerated":
        """Cast to another type.

        Returns:
            _Cast_BasicConicalGearMachineSettingsGenerated
        """
        return _Cast_BasicConicalGearMachineSettingsGenerated(self)
