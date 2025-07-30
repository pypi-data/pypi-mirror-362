"""NonLinearDQModelMultipleOperatingPointsLoadCase"""

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
from mastapy._private.electric_machines.load_cases_and_analyses import _1543

_NON_LINEAR_DQ_MODEL_MULTIPLE_OPERATING_POINTS_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses",
    "NonLinearDQModelMultipleOperatingPointsLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.load_cases_and_analyses import (
        _1535,
        _1537,
        _1538,
        _1559,
    )

    Self = TypeVar("Self", bound="NonLinearDQModelMultipleOperatingPointsLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="NonLinearDQModelMultipleOperatingPointsLoadCase._Cast_NonLinearDQModelMultipleOperatingPointsLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("NonLinearDQModelMultipleOperatingPointsLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NonLinearDQModelMultipleOperatingPointsLoadCase:
    """Special nested class for casting NonLinearDQModelMultipleOperatingPointsLoadCase to subclasses."""

    __parent__: "NonLinearDQModelMultipleOperatingPointsLoadCase"

    @property
    def electric_machine_load_case_base(
        self: "CastSelf",
    ) -> "_1543.ElectricMachineLoadCaseBase":
        return self.__parent__._cast(_1543.ElectricMachineLoadCaseBase)

    @property
    def efficiency_map_load_case(self: "CastSelf") -> "_1535.EfficiencyMapLoadCase":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1535

        return self.__parent__._cast(_1535.EfficiencyMapLoadCase)

    @property
    def speed_torque_curve_load_case(
        self: "CastSelf",
    ) -> "_1559.SpeedTorqueCurveLoadCase":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1559

        return self.__parent__._cast(_1559.SpeedTorqueCurveLoadCase)

    @property
    def non_linear_dq_model_multiple_operating_points_load_case(
        self: "CastSelf",
    ) -> "NonLinearDQModelMultipleOperatingPointsLoadCase":
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
class NonLinearDQModelMultipleOperatingPointsLoadCase(
    _1543.ElectricMachineLoadCaseBase
):
    """NonLinearDQModelMultipleOperatingPointsLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NON_LINEAR_DQ_MODEL_MULTIPLE_OPERATING_POINTS_LOAD_CASE

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_NonLinearDQModelMultipleOperatingPointsLoadCase":
        """Cast to another type.

        Returns:
            _Cast_NonLinearDQModelMultipleOperatingPointsLoadCase
        """
        return _Cast_NonLinearDQModelMultipleOperatingPointsLoadCase(self)
