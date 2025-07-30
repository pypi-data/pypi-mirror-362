"""CradleStyleConicalMachineSettingsGenerated"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_CRADLE_STYLE_CONICAL_MACHINE_SETTINGS_GENERATED = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel.BasicMachineSettings",
    "CradleStyleConicalMachineSettingsGenerated",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CradleStyleConicalMachineSettingsGenerated")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CradleStyleConicalMachineSettingsGenerated._Cast_CradleStyleConicalMachineSettingsGenerated",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CradleStyleConicalMachineSettingsGenerated",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CradleStyleConicalMachineSettingsGenerated:
    """Special nested class for casting CradleStyleConicalMachineSettingsGenerated to subclasses."""

    __parent__: "CradleStyleConicalMachineSettingsGenerated"

    @property
    def cradle_style_conical_machine_settings_generated(
        self: "CastSelf",
    ) -> "CradleStyleConicalMachineSettingsGenerated":
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
class CradleStyleConicalMachineSettingsGenerated(_0.APIBase):
    """CradleStyleConicalMachineSettingsGenerated

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CRADLE_STYLE_CONICAL_MACHINE_SETTINGS_GENERATED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cradle_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CradleAngle")

        if temp is None:
            return 0.0

        return temp

    @cradle_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def cradle_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CradleAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def cutter_spindle_rotation_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CutterSpindleRotationAngle")

        if temp is None:
            return 0.0

        return temp

    @cutter_spindle_rotation_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def cutter_spindle_rotation_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CutterSpindleRotationAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def decimal_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DecimalRatio")

        if temp is None:
            return 0.0

        return temp

    @decimal_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def decimal_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DecimalRatio", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def eccentric_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EccentricAngle")

        if temp is None:
            return 0.0

        return temp

    @eccentric_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def eccentric_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EccentricAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def machine_centre_to_back(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MachineCentreToBack")

        if temp is None:
            return 0.0

        return temp

    @machine_centre_to_back.setter
    @exception_bridge
    @enforce_parameter_types
    def machine_centre_to_back(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MachineCentreToBack",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def machine_root_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MachineRootAngle")

        if temp is None:
            return 0.0

        return temp

    @machine_root_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def machine_root_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MachineRootAngle", float(value) if value is not None else 0.0
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
    def sliding_base(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SlidingBase")

        if temp is None:
            return 0.0

        return temp

    @sliding_base.setter
    @exception_bridge
    @enforce_parameter_types
    def sliding_base(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SlidingBase", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def swivel_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SwivelAngle")

        if temp is None:
            return 0.0

        return temp

    @swivel_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def swivel_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SwivelAngle", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CradleStyleConicalMachineSettingsGenerated":
        """Cast to another type.

        Returns:
            _Cast_CradleStyleConicalMachineSettingsGenerated
        """
        return _Cast_CradleStyleConicalMachineSettingsGenerated(self)
