"""SpeedTorqueLoadCase"""

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
from mastapy._private.electric_machines.load_cases_and_analyses import _1542

_SPEED_TORQUE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "SpeedTorqueLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.load_cases_and_analyses import (
        _1537,
        _1538,
        _1543,
        _1556,
    )

    Self = TypeVar("Self", bound="SpeedTorqueLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="SpeedTorqueLoadCase._Cast_SpeedTorqueLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpeedTorqueLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpeedTorqueLoadCase:
    """Special nested class for casting SpeedTorqueLoadCase to subclasses."""

    __parent__: "SpeedTorqueLoadCase"

    @property
    def electric_machine_load_case(self: "CastSelf") -> "_1542.ElectricMachineLoadCase":
        return self.__parent__._cast(_1542.ElectricMachineLoadCase)

    @property
    def electric_machine_load_case_base(
        self: "CastSelf",
    ) -> "_1543.ElectricMachineLoadCaseBase":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1543

        return self.__parent__._cast(_1543.ElectricMachineLoadCaseBase)

    @property
    def speed_torque_load_case(self: "CastSelf") -> "SpeedTorqueLoadCase":
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
class SpeedTorqueLoadCase(_1542.ElectricMachineLoadCase):
    """SpeedTorqueLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPEED_TORQUE_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def control_strategy(self: "Self") -> "_1538.ElectricMachineControlStrategy":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineControlStrategy"""
        temp = pythonnet_property_get(self.wrapped, "ControlStrategy")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.ElectricMachineControlStrategy",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.load_cases_and_analyses._1538",
            "ElectricMachineControlStrategy",
        )(value)

    @control_strategy.setter
    @exception_bridge
    @enforce_parameter_types
    def control_strategy(
        self: "Self", value: "_1538.ElectricMachineControlStrategy"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.ElectricMachineControlStrategy",
        )
        pythonnet_property_set(self.wrapped, "ControlStrategy", value)

    @property
    @exception_bridge
    def include_resistive_voltages(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeResistiveVoltages")

        if temp is None:
            return False

        return temp

    @include_resistive_voltages.setter
    @exception_bridge
    @enforce_parameter_types
    def include_resistive_voltages(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeResistiveVoltages",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def load_specification(self: "Self") -> "_1556.SpecifyTorqueOrCurrent":
        """mastapy.electric_machines.load_cases_and_analyses.SpecifyTorqueOrCurrent"""
        temp = pythonnet_property_get(self.wrapped, "LoadSpecification")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.SpecifyTorqueOrCurrent",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.load_cases_and_analyses._1556",
            "SpecifyTorqueOrCurrent",
        )(value)

    @load_specification.setter
    @exception_bridge
    @enforce_parameter_types
    def load_specification(self: "Self", value: "_1556.SpecifyTorqueOrCurrent") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.SpecifyTorqueOrCurrent",
        )
        pythonnet_property_set(self.wrapped, "LoadSpecification", value)

    @property
    @exception_bridge
    def target_torque(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TargetTorque")

        if temp is None:
            return 0.0

        return temp

    @target_torque.setter
    @exception_bridge
    @enforce_parameter_types
    def target_torque(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TargetTorque", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def basic_mechanical_loss_settings(
        self: "Self",
    ) -> "_1537.ElectricMachineBasicMechanicalLossSettings":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineBasicMechanicalLossSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicMechanicalLossSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpeedTorqueLoadCase":
        """Cast to another type.

        Returns:
            _Cast_SpeedTorqueLoadCase
        """
        return _Cast_SpeedTorqueLoadCase(self)
