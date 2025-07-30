"""BasicDynamicForceLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.load_cases_and_analyses import _1543
from mastapy._private.nodal_analysis.elmer import _249

_BASIC_DYNAMIC_FORCE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "BasicDynamicForceLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines import _1394
    from mastapy._private.electric_machines.load_cases_and_analyses import (
        _1531,
        _1532,
        _1533,
        _1552,
    )

    Self = TypeVar("Self", bound="BasicDynamicForceLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="BasicDynamicForceLoadCase._Cast_BasicDynamicForceLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BasicDynamicForceLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BasicDynamicForceLoadCase:
    """Special nested class for casting BasicDynamicForceLoadCase to subclasses."""

    __parent__: "BasicDynamicForceLoadCase"

    @property
    def electric_machine_load_case_base(
        self: "CastSelf",
    ) -> "_1543.ElectricMachineLoadCaseBase":
        return self.__parent__._cast(_1543.ElectricMachineLoadCaseBase)

    @property
    def dynamic_force_load_case(self: "CastSelf") -> "_1532.DynamicForceLoadCase":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1532

        return self.__parent__._cast(_1532.DynamicForceLoadCase)

    @property
    def basic_dynamic_force_load_case(self: "CastSelf") -> "BasicDynamicForceLoadCase":
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
class BasicDynamicForceLoadCase(_1543.ElectricMachineLoadCaseBase):
    """BasicDynamicForceLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BASIC_DYNAMIC_FORCE_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def analysis_period(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ElectricMachineAnalysisPeriod":
        """EnumWithSelectedValue[mastapy.nodal_analysis.elmer.ElectricMachineAnalysisPeriod]"""
        temp = pythonnet_property_get(self.wrapped, "AnalysisPeriod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ElectricMachineAnalysisPeriod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @analysis_period.setter
    @exception_bridge
    @enforce_parameter_types
    def analysis_period(
        self: "Self", value: "_249.ElectricMachineAnalysisPeriod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ElectricMachineAnalysisPeriod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "AnalysisPeriod", value)

    @property
    @exception_bridge
    def keep_single_operating_point_results(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "KeepSingleOperatingPointResults")

        if temp is None:
            return False

        return temp

    @keep_single_operating_point_results.setter
    @exception_bridge
    @enforce_parameter_types
    def keep_single_operating_point_results(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "KeepSingleOperatingPointResults",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def number_of_steps_per_operating_point_specification_method(
        self: "Self",
    ) -> "_1552.NumberOfStepsPerOperatingPointSpecificationMethod":
        """mastapy.electric_machines.load_cases_and_analyses.NumberOfStepsPerOperatingPointSpecificationMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfStepsPerOperatingPointSpecificationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.NumberOfStepsPerOperatingPointSpecificationMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.load_cases_and_analyses._1552",
            "NumberOfStepsPerOperatingPointSpecificationMethod",
        )(value)

    @number_of_steps_per_operating_point_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_steps_per_operating_point_specification_method(
        self: "Self", value: "_1552.NumberOfStepsPerOperatingPointSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.NumberOfStepsPerOperatingPointSpecificationMethod",
        )
        pythonnet_property_set(
            self.wrapped, "NumberOfStepsPerOperatingPointSpecificationMethod", value
        )

    @property
    @exception_bridge
    def number_of_steps_for_the_analysis_period(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfStepsForTheAnalysisPeriod")

        if temp is None:
            return 0

        return temp

    @number_of_steps_for_the_analysis_period.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_steps_for_the_analysis_period(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfStepsForTheAnalysisPeriod",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def operating_points(self: "Self") -> "List[_1533.DynamicForcesOperatingPoint]":
        """List[mastapy.electric_machines.load_cases_and_analyses.DynamicForcesOperatingPoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def add_operating_point(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddOperatingPoint")

    @exception_bridge
    @enforce_parameter_types
    def add_operating_point_specified_by_peak_current_and_current_angle(
        self: "Self", peak_current: "float", current_angle: "float", speed: "float"
    ) -> "_1533.DynamicForcesOperatingPoint":
        """mastapy.electric_machines.load_cases_and_analyses.DynamicForcesOperatingPoint

        Args:
            peak_current (float)
            current_angle (float)
            speed (float)
        """
        peak_current = float(peak_current)
        current_angle = float(current_angle)
        speed = float(speed)
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddOperatingPointSpecifiedByPeakCurrentAndCurrentAngle",
            peak_current if peak_current else 0.0,
            current_angle if current_angle else 0.0,
            speed if speed else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def analysis_for(
        self: "Self", setup: "_1394.ElectricMachineSetup"
    ) -> "_1531.DynamicForceAnalysis":
        """mastapy.electric_machines.load_cases_and_analyses.DynamicForceAnalysis

        Args:
            setup (mastapy.electric_machines.ElectricMachineSetup)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "AnalysisFor", setup.wrapped if setup else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def remove_operating_point(
        self: "Self", operating_point: "_1533.DynamicForcesOperatingPoint"
    ) -> None:
        """Method does not return.

        Args:
            operating_point (mastapy.electric_machines.load_cases_and_analyses.DynamicForcesOperatingPoint)
        """
        pythonnet_method_call(
            self.wrapped,
            "RemoveOperatingPoint",
            operating_point.wrapped if operating_point else None,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BasicDynamicForceLoadCase":
        """Cast to another type.

        Returns:
            _Cast_BasicDynamicForceLoadCase
        """
        return _Cast_BasicDynamicForceLoadCase(self)
