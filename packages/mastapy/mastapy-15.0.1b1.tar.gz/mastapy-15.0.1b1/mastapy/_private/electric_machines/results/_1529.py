"""OpenCircuitElectricMachineResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines.results import _1510

_OPEN_CIRCUIT_ELECTRIC_MACHINE_RESULTS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results", "OpenCircuitElectricMachineResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OpenCircuitElectricMachineResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="OpenCircuitElectricMachineResults._Cast_OpenCircuitElectricMachineResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("OpenCircuitElectricMachineResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OpenCircuitElectricMachineResults:
    """Special nested class for casting OpenCircuitElectricMachineResults to subclasses."""

    __parent__: "OpenCircuitElectricMachineResults"

    @property
    def electric_machine_results(self: "CastSelf") -> "_1510.ElectricMachineResults":
        return self.__parent__._cast(_1510.ElectricMachineResults)

    @property
    def open_circuit_electric_machine_results(
        self: "CastSelf",
    ) -> "OpenCircuitElectricMachineResults":
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
class OpenCircuitElectricMachineResults(_1510.ElectricMachineResults):
    """OpenCircuitElectricMachineResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OPEN_CIRCUIT_ELECTRIC_MACHINE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def back_emf_constant(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BackEMFConstant")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def line_to_line_back_emf_peak(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LineToLineBackEMFPeak")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def line_to_line_back_emfrms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LineToLineBackEMFRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def line_to_line_back_emf_total_harmonic_distortion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LineToLineBackEMFTotalHarmonicDistortion"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def phase_back_emf_peak(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseBackEMFPeak")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def phase_back_emfrms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseBackEMFRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def phase_back_emf_total_harmonic_distortion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PhaseBackEMFTotalHarmonicDistortion"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_OpenCircuitElectricMachineResults":
        """Cast to another type.

        Returns:
            _Cast_OpenCircuitElectricMachineResults
        """
        return _Cast_OpenCircuitElectricMachineResults(self)
