"""SingleOperatingPointAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines.load_cases_and_analyses import _1536

_SINGLE_OPERATING_POINT_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "SingleOperatingPointAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines.load_cases_and_analyses import (
        _1540,
        _1542,
        _1555,
    )
    from mastapy._private.electric_machines.results import _1514

    Self = TypeVar("Self", bound="SingleOperatingPointAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SingleOperatingPointAnalysis._Cast_SingleOperatingPointAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SingleOperatingPointAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SingleOperatingPointAnalysis:
    """Special nested class for casting SingleOperatingPointAnalysis to subclasses."""

    __parent__: "SingleOperatingPointAnalysis"

    @property
    def electric_machine_analysis(self: "CastSelf") -> "_1536.ElectricMachineAnalysis":
        return self.__parent__._cast(_1536.ElectricMachineAnalysis)

    @property
    def electric_machine_fe_analysis(
        self: "CastSelf",
    ) -> "_1540.ElectricMachineFEAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1540

        return self.__parent__._cast(_1540.ElectricMachineFEAnalysis)

    @property
    def single_operating_point_analysis(
        self: "CastSelf",
    ) -> "SingleOperatingPointAnalysis":
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
class SingleOperatingPointAnalysis(_1536.ElectricMachineAnalysis):
    """SingleOperatingPointAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SINGLE_OPERATING_POINT_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def current_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def d_axis_current(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DAxisCurrent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def electrical_frequency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricalFrequency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def electrical_period(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricalPeriod")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def field_winding_current(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FieldWindingCurrent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mechanical_period(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MechanicalPeriod")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peak_line_current(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakLineCurrent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peak_phase_current(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakPhaseCurrent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def phase_current_drms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseCurrentDRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def phase_current_qrms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseCurrentQRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def q_axis_current(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "QAxisCurrent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rms_phase_current(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RMSPhaseCurrent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def slot_passing_period(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlotPassingPeriod")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def time_step_increment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeStepIncrement")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def electric_machine_results(
        self: "Self",
    ) -> "_1514.ElectricMachineResultsForOpenCircuitAndOnLoad":
        """mastapy.electric_machines.results.ElectricMachineResultsForOpenCircuitAndOnLoad

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def load_case(self: "Self") -> "_1542.ElectricMachineLoadCase":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def slot_section_details_for_analysis(
        self: "Self",
    ) -> "List[_1555.SlotDetailForAnalysis]":
        """List[mastapy.electric_machines.load_cases_and_analyses.SlotDetailForAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlotSectionDetailsForAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SingleOperatingPointAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SingleOperatingPointAnalysis
        """
        return _Cast_SingleOperatingPointAnalysis(self)
