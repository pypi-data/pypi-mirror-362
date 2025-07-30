"""ElectricMachineMechanicalLoadCase"""

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

_ELECTRIC_MACHINE_MECHANICAL_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses",
    "ElectricMachineMechanicalLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.elmer import _257

    Self = TypeVar("Self", bound="ElectricMachineMechanicalLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineMechanicalLoadCase._Cast_ElectricMachineMechanicalLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineMechanicalLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineMechanicalLoadCase:
    """Special nested class for casting ElectricMachineMechanicalLoadCase to subclasses."""

    __parent__: "ElectricMachineMechanicalLoadCase"

    @property
    def electric_machine_load_case_base(
        self: "CastSelf",
    ) -> "_1543.ElectricMachineLoadCaseBase":
        return self.__parent__._cast(_1543.ElectricMachineLoadCaseBase)

    @property
    def electric_machine_mechanical_load_case(
        self: "CastSelf",
    ) -> "ElectricMachineMechanicalLoadCase":
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
class ElectricMachineMechanicalLoadCase(_1543.ElectricMachineLoadCaseBase):
    """ElectricMachineMechanicalLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_MECHANICAL_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def convergence_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ConvergenceTolerance")

        if temp is None:
            return 0.0

        return temp

    @convergence_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def convergence_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ConvergenceTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_iterations(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumIterations")

        if temp is None:
            return 0

        return temp

    @maximum_iterations.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_iterations(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumIterations", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def solver_type(self: "Self") -> "_257.MechanicalSolverType":
        """mastapy.nodal_analysis.elmer.MechanicalSolverType"""
        temp = pythonnet_property_get(self.wrapped, "SolverType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.Elmer.MechanicalSolverType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis.elmer._257", "MechanicalSolverType"
        )(value)

    @solver_type.setter
    @exception_bridge
    @enforce_parameter_types
    def solver_type(self: "Self", value: "_257.MechanicalSolverType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.Elmer.MechanicalSolverType"
        )
        pythonnet_property_set(self.wrapped, "SolverType", value)

    @property
    @exception_bridge
    def speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        return temp

    @speed.setter
    @exception_bridge
    @enforce_parameter_types
    def speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Speed", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineMechanicalLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineMechanicalLoadCase
        """
        return _Cast_ElectricMachineMechanicalLoadCase(self)
