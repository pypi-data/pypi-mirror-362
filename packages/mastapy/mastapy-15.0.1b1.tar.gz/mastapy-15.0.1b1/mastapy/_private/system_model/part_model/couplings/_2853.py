"""TorqueConverter"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.system_model.part_model.couplings import _2823

_TORQUE_CONVERTER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverter"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2659, _2698, _2708
    from mastapy._private.system_model.part_model.couplings import _2854, _2856

    Self = TypeVar("Self", bound="TorqueConverter")
    CastSelf = TypeVar("CastSelf", bound="TorqueConverter._Cast_TorqueConverter")


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverter:
    """Special nested class for casting TorqueConverter to subclasses."""

    __parent__: "TorqueConverter"

    @property
    def coupling(self: "CastSelf") -> "_2823.Coupling":
        return self.__parent__._cast(_2823.Coupling)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2708.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2708

        return self.__parent__._cast(_2708.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2659

        return self.__parent__._cast(_2659.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def torque_converter(self: "CastSelf") -> "TorqueConverter":
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
class TorqueConverter(_2823.Coupling):
    """TorqueConverter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_CONVERTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def clutch_to_oil_heat_transfer_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ClutchToOilHeatTransferCoefficient"
        )

        if temp is None:
            return 0.0

        return temp

    @clutch_to_oil_heat_transfer_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def clutch_to_oil_heat_transfer_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ClutchToOilHeatTransferCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def has_lock_up_clutch(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasLockUpClutch")

        if temp is None:
            return False

        return temp

    @has_lock_up_clutch.setter
    @exception_bridge
    @enforce_parameter_types
    def has_lock_up_clutch(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HasLockUpClutch", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def heat_transfer_area(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HeatTransferArea")

        if temp is None:
            return 0.0

        return temp

    @heat_transfer_area.setter
    @exception_bridge
    @enforce_parameter_types
    def heat_transfer_area(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HeatTransferArea", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def specific_heat_capacity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecificHeatCapacity")

        if temp is None:
            return 0.0

        return temp

    @specific_heat_capacity.setter
    @exception_bridge
    @enforce_parameter_types
    def specific_heat_capacity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecificHeatCapacity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def static_to_dynamic_friction_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StaticToDynamicFrictionRatio")

        if temp is None:
            return 0.0

        return temp

    @static_to_dynamic_friction_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def static_to_dynamic_friction_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StaticToDynamicFrictionRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def thermal_mass(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ThermalMass")

        if temp is None:
            return 0.0

        return temp

    @thermal_mass.setter
    @exception_bridge
    @enforce_parameter_types
    def thermal_mass(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ThermalMass", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tolerance_for_speed_ratio_of_unity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceForSpeedRatioOfUnity")

        if temp is None:
            return 0.0

        return temp

    @tolerance_for_speed_ratio_of_unity.setter
    @exception_bridge
    @enforce_parameter_types
    def tolerance_for_speed_ratio_of_unity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceForSpeedRatioOfUnity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def torque_capacity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TorqueCapacity")

        if temp is None:
            return 0.0

        return temp

    @torque_capacity.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_capacity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TorqueCapacity", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def pump(self: "Self") -> "_2854.TorqueConverterPump":
        """mastapy.system_model.part_model.couplings.TorqueConverterPump

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Pump")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def turbine(self: "Self") -> "_2856.TorqueConverterTurbine":
        """mastapy.system_model.part_model.couplings.TorqueConverterTurbine

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Turbine")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_TorqueConverter":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverter
        """
        return _Cast_TorqueConverter(self)
