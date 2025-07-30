"""BasicConicalGearMachineSettingsFormate"""

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

_BASIC_CONICAL_GEAR_MACHINE_SETTINGS_FORMATE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel.BasicMachineSettings",
    "BasicConicalGearMachineSettingsFormate",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BasicConicalGearMachineSettingsFormate")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BasicConicalGearMachineSettingsFormate._Cast_BasicConicalGearMachineSettingsFormate",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BasicConicalGearMachineSettingsFormate",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BasicConicalGearMachineSettingsFormate:
    """Special nested class for casting BasicConicalGearMachineSettingsFormate to subclasses."""

    __parent__: "BasicConicalGearMachineSettingsFormate"

    @property
    def basic_conical_gear_machine_settings(
        self: "CastSelf",
    ) -> "_924.BasicConicalGearMachineSettings":
        return self.__parent__._cast(_924.BasicConicalGearMachineSettings)

    @property
    def basic_conical_gear_machine_settings_formate(
        self: "CastSelf",
    ) -> "BasicConicalGearMachineSettingsFormate":
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
class BasicConicalGearMachineSettingsFormate(_924.BasicConicalGearMachineSettings):
    """BasicConicalGearMachineSettingsFormate

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BASIC_CONICAL_GEAR_MACHINE_SETTINGS_FORMATE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def horizontal_setting(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HorizontalSetting")

        if temp is None:
            return 0.0

        return temp

    @horizontal_setting.setter
    @exception_bridge
    @enforce_parameter_types
    def horizontal_setting(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HorizontalSetting",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def vertical_setting(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VerticalSetting")

        if temp is None:
            return 0.0

        return temp

    @vertical_setting.setter
    @exception_bridge
    @enforce_parameter_types
    def vertical_setting(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "VerticalSetting", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BasicConicalGearMachineSettingsFormate":
        """Cast to another type.

        Returns:
            _Cast_BasicConicalGearMachineSettingsFormate
        """
        return _Cast_BasicConicalGearMachineSettingsFormate(self)
