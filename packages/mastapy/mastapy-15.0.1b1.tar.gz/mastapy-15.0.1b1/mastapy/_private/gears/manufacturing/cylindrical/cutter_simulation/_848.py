"""ShaperSimulationCalculator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _834

_SHAPER_SIMULATION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "ShaperSimulationCalculator",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _829

    Self = TypeVar("Self", bound="ShaperSimulationCalculator")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaperSimulationCalculator._Cast_ShaperSimulationCalculator"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaperSimulationCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaperSimulationCalculator:
    """Special nested class for casting ShaperSimulationCalculator to subclasses."""

    __parent__: "ShaperSimulationCalculator"

    @property
    def cutter_simulation_calc(self: "CastSelf") -> "_834.CutterSimulationCalc":
        return self.__parent__._cast(_834.CutterSimulationCalc)

    @property
    def shaper_simulation_calculator(self: "CastSelf") -> "ShaperSimulationCalculator":
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
class ShaperSimulationCalculator(_834.CutterSimulationCalc):
    """ShaperSimulationCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAPER_SIMULATION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cutting_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CuttingCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cutting_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CuttingPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaper_sap_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaperSAPDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaper(self: "Self") -> "_829.CylindricalGearShaperTangible":
        """mastapy.gears.manufacturing.cylindrical.cutters.tangibles.CylindricalGearShaperTangible

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shaper")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaperSimulationCalculator":
        """Cast to another type.

        Returns:
            _Cast_ShaperSimulationCalculator
        """
        return _Cast_ShaperSimulationCalculator(self)
