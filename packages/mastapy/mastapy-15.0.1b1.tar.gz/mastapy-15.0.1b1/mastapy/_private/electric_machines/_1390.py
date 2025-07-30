"""ElectricMachineGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ELECTRIC_MACHINE_GROUP = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "ElectricMachineGroup"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines import _1387, _1397, _1421
    from mastapy._private.electric_machines.load_cases_and_analyses import _1544
    from mastapy._private.electric_machines.thermal import _1480

    Self = TypeVar("Self", bound="ElectricMachineGroup")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineGroup._Cast_ElectricMachineGroup"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineGroup:
    """Special nested class for casting ElectricMachineGroup to subclasses."""

    __parent__: "ElectricMachineGroup"

    @property
    def electric_machine_group(self: "CastSelf") -> "ElectricMachineGroup":
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
class ElectricMachineGroup(_0.APIBase):
    """ElectricMachineGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def electric_machine_details(self: "Self") -> "List[_1387.ElectricMachineDetail]":
        """List[mastapy.electric_machines.ElectricMachineDetail]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def electric_machine_load_case_groups(
        self: "Self",
    ) -> "List[_1544.ElectricMachineLoadCaseGroup]":
        """List[mastapy.electric_machines.load_cases_and_analyses.ElectricMachineLoadCaseGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineLoadCaseGroups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def thermal_electric_machines(self: "Self") -> "List[_1480.ThermalElectricMachine]":
        """List[mastapy.electric_machines.thermal.ThermalElectricMachine]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalElectricMachines")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def add_electric_machine_detail(
        self: "Self", type_: "_1397.ElectricMachineType", name: "str" = "Motor"
    ) -> "_1421.NonCADElectricMachineDetail":
        """mastapy.electric_machines.NonCADElectricMachineDetail

        Args:
            type_ (mastapy.electric_machines.ElectricMachineType)
            name (str, optional)
        """
        type_ = conversion.mp_to_pn_enum(
            type_, "SMT.MastaAPI.ElectricMachines.ElectricMachineType"
        )
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddElectricMachineDetail", type_, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_load_case_group(
        self: "Self", name: "str" = "New Load Case Group"
    ) -> "_1544.ElectricMachineLoadCaseGroup":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineLoadCaseGroup

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddLoadCaseGroup", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_thermal_electric_machine(
        self: "Self", electric_machine: "_1387.ElectricMachineDetail", name: "str"
    ) -> "_1480.ThermalElectricMachine":
        """mastapy.electric_machines.thermal.ThermalElectricMachine

        Args:
            electric_machine (mastapy.electric_machines.ElectricMachineDetail)
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddThermalElectricMachine",
            electric_machine.wrapped if electric_machine else None,
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def duplicate_electric_machine_detail(
        self: "Self", detail: "_1387.ElectricMachineDetail"
    ) -> "_1387.ElectricMachineDetail":
        """mastapy.electric_machines.ElectricMachineDetail

        Args:
            detail (mastapy.electric_machines.ElectricMachineDetail)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "DuplicateElectricMachineDetail",
            detail.wrapped if detail else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def duplicate_thermal_electric_machine(
        self: "Self", thermal_electric_machine: "_1480.ThermalElectricMachine"
    ) -> "_1480.ThermalElectricMachine":
        """mastapy.electric_machines.thermal.ThermalElectricMachine

        Args:
            thermal_electric_machine (mastapy.electric_machines.thermal.ThermalElectricMachine)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "DuplicateThermalElectricMachine",
            thermal_electric_machine.wrapped if thermal_electric_machine else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def electric_machine_detail_named(
        self: "Self", name: "str", has_non_linear_dq_model: "bool"
    ) -> "_1387.ElectricMachineDetail":
        """mastapy.electric_machines.ElectricMachineDetail

        Args:
            name (str)
            has_non_linear_dq_model (bool)
        """
        name = str(name)
        has_non_linear_dq_model = bool(has_non_linear_dq_model)
        method_result = pythonnet_method_call(
            self.wrapped,
            "ElectricMachineDetailNamed",
            name if name else "",
            has_non_linear_dq_model if has_non_linear_dq_model else False,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def load_case_group_named(
        self: "Self", load_case_group_name: "str"
    ) -> "_1544.ElectricMachineLoadCaseGroup":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineLoadCaseGroup

        Args:
            load_case_group_name (str)
        """
        load_case_group_name = str(load_case_group_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "LoadCaseGroupNamed",
            load_case_group_name if load_case_group_name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def remove_all_electric_machine_details(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveAllElectricMachineDetails")

    @exception_bridge
    def remove_all_load_case_groups(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveAllLoadCaseGroups")

    @exception_bridge
    def remove_all_thermal_electric_machine(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveAllThermalElectricMachine")

    @exception_bridge
    @enforce_parameter_types
    def remove_electric_machine_detail(
        self: "Self", motor: "_1387.ElectricMachineDetail"
    ) -> "bool":
        """bool

        Args:
            motor (mastapy.electric_machines.ElectricMachineDetail)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "RemoveElectricMachineDetail",
            motor.wrapped if motor else None,
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def remove_electric_machine_detail_named(
        self: "Self", name: "str", has_non_linear_dq_model: "bool"
    ) -> "bool":
        """bool

        Args:
            name (str)
            has_non_linear_dq_model (bool)
        """
        name = str(name)
        has_non_linear_dq_model = bool(has_non_linear_dq_model)
        method_result = pythonnet_method_call(
            self.wrapped,
            "RemoveElectricMachineDetailNamed",
            name if name else "",
            has_non_linear_dq_model if has_non_linear_dq_model else False,
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def remove_load_case_group_named(self: "Self", name: "str") -> "bool":
        """bool

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "RemoveLoadCaseGroupNamed", name if name else ""
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def remove_thermal_electric_machine(
        self: "Self", thermal_electric_machine: "_1480.ThermalElectricMachine"
    ) -> "bool":
        """bool

        Args:
            thermal_electric_machine (mastapy.electric_machines.thermal.ThermalElectricMachine)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "RemoveThermalElectricMachine",
            thermal_electric_machine.wrapped if thermal_electric_machine else None,
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def remove_thermal_electric_machine_named(self: "Self", name: "str") -> "bool":
        """bool

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "RemoveThermalElectricMachineNamed", name if name else ""
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def thermal_electric_machine_named(
        self: "Self", name: "str"
    ) -> "_1480.ThermalElectricMachine":
        """mastapy.electric_machines.thermal.ThermalElectricMachine

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "ThermalElectricMachineNamed", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def try_remove_load_case_group(
        self: "Self", load_case_group: "_1544.ElectricMachineLoadCaseGroup"
    ) -> "bool":
        """bool

        Args:
            load_case_group (mastapy.electric_machines.load_cases_and_analyses.ElectricMachineLoadCaseGroup)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryRemoveLoadCaseGroup",
            load_case_group.wrapped if load_case_group else None,
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineGroup":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineGroup
        """
        return _Cast_ElectricMachineGroup(self)
