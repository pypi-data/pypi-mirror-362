"""OilPumpDetail"""

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
from mastapy._private.utility import _1779

_OIL_PUMP_DETAIL = python_net_import(
    "SMT.MastaAPI.Materials.Efficiency", "OilPumpDetail"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.materials.efficiency import _388
    from mastapy._private.math_utility import _1718

    Self = TypeVar("Self", bound="OilPumpDetail")
    CastSelf = TypeVar("CastSelf", bound="OilPumpDetail._Cast_OilPumpDetail")


__docformat__ = "restructuredtext en"
__all__ = ("OilPumpDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OilPumpDetail:
    """Special nested class for casting OilPumpDetail to subclasses."""

    __parent__: "OilPumpDetail"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def oil_pump_detail(self: "CastSelf") -> "OilPumpDetail":
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
class OilPumpDetail(_1779.IndependentReportablePropertiesBase["OilPumpDetail"]):
    """OilPumpDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OIL_PUMP_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def electric_motor_efficiency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ElectricMotorEfficiency")

        if temp is None:
            return 0.0

        return temp

    @electric_motor_efficiency.setter
    @exception_bridge
    @enforce_parameter_types
    def electric_motor_efficiency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ElectricMotorEfficiency",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def electric_power_consumed_vs_speed(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "ElectricPowerConsumedVsSpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @electric_power_consumed_vs_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def electric_power_consumed_vs_speed(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "ElectricPowerConsumedVsSpeed", value.wrapped
        )

    @property
    @exception_bridge
    def oil_flow_rate_vs_speed(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "OilFlowRateVsSpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @oil_flow_rate_vs_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def oil_flow_rate_vs_speed(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "OilFlowRateVsSpeed", value.wrapped)

    @property
    @exception_bridge
    def oil_pump_drive_type(self: "Self") -> "_388.OilPumpDriveType":
        """mastapy.materials.efficiency.OilPumpDriveType"""
        temp = pythonnet_property_get(self.wrapped, "OilPumpDriveType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.Efficiency.OilPumpDriveType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials.efficiency._388", "OilPumpDriveType"
        )(value)

    @oil_pump_drive_type.setter
    @exception_bridge
    @enforce_parameter_types
    def oil_pump_drive_type(self: "Self", value: "_388.OilPumpDriveType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.Efficiency.OilPumpDriveType"
        )
        pythonnet_property_set(self.wrapped, "OilPumpDriveType", value)

    @property
    @exception_bridge
    def oil_pump_efficiency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OilPumpEfficiency")

        if temp is None:
            return 0.0

        return temp

    @oil_pump_efficiency.setter
    @exception_bridge
    @enforce_parameter_types
    def oil_pump_efficiency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OilPumpEfficiency",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def operating_oil_pressure_vs_speed(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "OperatingOilPressureVsSpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @operating_oil_pressure_vs_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def operating_oil_pressure_vs_speed(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "OperatingOilPressureVsSpeed", value.wrapped
        )

    @property
    def cast_to(self: "Self") -> "_Cast_OilPumpDetail":
        """Cast to another type.

        Returns:
            _Cast_OilPumpDetail
        """
        return _Cast_OilPumpDetail(self)
