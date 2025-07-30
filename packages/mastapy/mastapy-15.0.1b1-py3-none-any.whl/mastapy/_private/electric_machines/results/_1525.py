"""MaximumTorqueResultsPoints"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_MAXIMUM_TORQUE_RESULTS_POINTS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results", "MaximumTorqueResultsPoints"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MaximumTorqueResultsPoints")
    CastSelf = TypeVar(
        "CastSelf", bound="MaximumTorqueResultsPoints._Cast_MaximumTorqueResultsPoints"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MaximumTorqueResultsPoints",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MaximumTorqueResultsPoints:
    """Special nested class for casting MaximumTorqueResultsPoints to subclasses."""

    __parent__: "MaximumTorqueResultsPoints"

    @property
    def maximum_torque_results_points(self: "CastSelf") -> "MaximumTorqueResultsPoints":
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
class MaximumTorqueResultsPoints(_0.APIBase):
    """MaximumTorqueResultsPoints

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MAXIMUM_TORQUE_RESULTS_POINTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActivePower")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def apparent_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ApparentPower")

        if temp is None:
            return 0.0

        return temp

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
    def d_axis_flux_linkage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DAxisFluxLinkage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def d_axis_voltage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DAxisVoltage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dc_winding_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DCWindingLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def electrical_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricalSpeed")

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
    def field_winding_dc_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FieldWindingDCLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def field_winding_flux_linkage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FieldWindingFluxLinkage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peak_phase_current_magnitude(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakPhaseCurrentMagnitude")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peak_phase_voltage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakPhaseVoltage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Power")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFactor")

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
    def q_axis_flux_linkage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "QAxisFluxLinkage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def q_axis_voltage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "QAxisVoltage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Torque")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_MaximumTorqueResultsPoints":
        """Cast to another type.

        Returns:
            _Cast_MaximumTorqueResultsPoints
        """
        return _Cast_MaximumTorqueResultsPoints(self)
