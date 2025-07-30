"""ShavingSimulationCalculator"""

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
from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _834

_SHAVING_SIMULATION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "ShavingSimulationCalculator",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShavingSimulationCalculator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShavingSimulationCalculator._Cast_ShavingSimulationCalculator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShavingSimulationCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShavingSimulationCalculator:
    """Special nested class for casting ShavingSimulationCalculator to subclasses."""

    __parent__: "ShavingSimulationCalculator"

    @property
    def cutter_simulation_calc(self: "CastSelf") -> "_834.CutterSimulationCalc":
        return self.__parent__._cast(_834.CutterSimulationCalc)

    @property
    def shaving_simulation_calculator(
        self: "CastSelf",
    ) -> "ShavingSimulationCalculator":
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
class ShavingSimulationCalculator(_834.CutterSimulationCalc):
    """ShavingSimulationCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAVING_SIMULATION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cross_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CrossAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_normal_shaving_pitch_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearNormalShavingPitchPressureAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_transverse_shaving_pitch_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearTransverseShavingPitchPressureAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def least_centre_distance_cross_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeastCentreDistanceCrossAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaver_transverse_shaving_pitch_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaverTransverseShavingPitchPressureAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaving_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShavingCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def theoretical_shaving_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TheoreticalShavingContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ShavingSimulationCalculator":
        """Cast to another type.

        Returns:
            _Cast_ShavingSimulationCalculator
        """
        return _Cast_ShavingSimulationCalculator(self)
