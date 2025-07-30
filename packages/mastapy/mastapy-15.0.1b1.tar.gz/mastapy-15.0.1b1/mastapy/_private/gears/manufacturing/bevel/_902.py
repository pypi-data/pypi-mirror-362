"""ManufacturingMachine"""

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
from mastapy._private.utility.databases import _2028

_MANUFACTURING_MACHINE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ManufacturingMachine"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.bevel import _901, _915

    Self = TypeVar("Self", bound="ManufacturingMachine")
    CastSelf = TypeVar(
        "CastSelf", bound="ManufacturingMachine._Cast_ManufacturingMachine"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ManufacturingMachine",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ManufacturingMachine:
    """Special nested class for casting ManufacturingMachine to subclasses."""

    __parent__: "ManufacturingMachine"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def manufacturing_machine(self: "CastSelf") -> "ManufacturingMachine":
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
class ManufacturingMachine(_2028.NamedDatabaseItem):
    """ManufacturingMachine

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MANUFACTURING_MACHINE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def can_work_for_formate(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CanWorkForFormate")

        if temp is None:
            return False

        return temp

    @can_work_for_formate.setter
    @exception_bridge
    @enforce_parameter_types
    def can_work_for_formate(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CanWorkForFormate",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def can_work_for_generating(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CanWorkForGenerating")

        if temp is None:
            return False

        return temp

    @can_work_for_generating.setter
    @exception_bridge
    @enforce_parameter_types
    def can_work_for_generating(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CanWorkForGenerating",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def can_work_for_roller_modification(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CanWorkForRollerModification")

        if temp is None:
            return False

        return temp

    @can_work_for_roller_modification.setter
    @exception_bridge
    @enforce_parameter_types
    def can_work_for_roller_modification(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CanWorkForRollerModification",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def can_work_for_tilt(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CanWorkForTilt")

        if temp is None:
            return False

        return temp

    @can_work_for_tilt.setter
    @exception_bridge
    @enforce_parameter_types
    def can_work_for_tilt(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "CanWorkForTilt", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def eccentric_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EccentricDistance")

        if temp is None:
            return 0.0

        return temp

    @eccentric_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def eccentric_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EccentricDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def machine_type(self: "Self") -> "_901.MachineTypes":
        """mastapy.gears.manufacturing.bevel.MachineTypes"""
        temp = pythonnet_property_get(self.wrapped, "MachineType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Manufacturing.Bevel.MachineTypes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.manufacturing.bevel._901", "MachineTypes"
        )(value)

    @machine_type.setter
    @exception_bridge
    @enforce_parameter_types
    def machine_type(self: "Self", value: "_901.MachineTypes") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Manufacturing.Bevel.MachineTypes"
        )
        pythonnet_property_set(self.wrapped, "MachineType", value)

    @property
    @exception_bridge
    def maximum_tilt_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumTiltAngle")

        if temp is None:
            return 0.0

        return temp

    @maximum_tilt_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_tilt_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumTiltAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tilt_body_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltBodyAngle")

        if temp is None:
            return 0.0

        return temp

    @tilt_body_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_body_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltBodyAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tilt_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltDistance")

        if temp is None:
            return 0.0

        return temp

    @tilt_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltDistance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def wheel_formate_machine_type(self: "Self") -> "_915.WheelFormatMachineTypes":
        """mastapy.gears.manufacturing.bevel.WheelFormatMachineTypes"""
        temp = pythonnet_property_get(self.wrapped, "WheelFormateMachineType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Manufacturing.Bevel.WheelFormatMachineTypes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.manufacturing.bevel._915", "WheelFormatMachineTypes"
        )(value)

    @wheel_formate_machine_type.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_formate_machine_type(
        self: "Self", value: "_915.WheelFormatMachineTypes"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Manufacturing.Bevel.WheelFormatMachineTypes"
        )
        pythonnet_property_set(self.wrapped, "WheelFormateMachineType", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ManufacturingMachine":
        """Cast to another type.

        Returns:
            _Cast_ManufacturingMachine
        """
        return _Cast_ManufacturingMachine(self)
