"""HobSimulationCalculator"""

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
from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _846

_HOB_SIMULATION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "HobSimulationCalculator",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _834
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _828

    Self = TypeVar("Self", bound="HobSimulationCalculator")
    CastSelf = TypeVar(
        "CastSelf", bound="HobSimulationCalculator._Cast_HobSimulationCalculator"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HobSimulationCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HobSimulationCalculator:
    """Special nested class for casting HobSimulationCalculator to subclasses."""

    __parent__: "HobSimulationCalculator"

    @property
    def rack_simulation_calculator(self: "CastSelf") -> "_846.RackSimulationCalculator":
        return self.__parent__._cast(_846.RackSimulationCalculator)

    @property
    def cutter_simulation_calc(self: "CastSelf") -> "_834.CutterSimulationCalc":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _834,
        )

        return self.__parent__._cast(_834.CutterSimulationCalc)

    @property
    def hob_simulation_calculator(self: "CastSelf") -> "HobSimulationCalculator":
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
class HobSimulationCalculator(_846.RackSimulationCalculator):
    """HobSimulationCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HOB_SIMULATION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def hob(self: "Self") -> "_828.CylindricalGearHobShape":
        """mastapy.gears.manufacturing.cylindrical.cutters.tangibles.CylindricalGearHobShape

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Hob")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_HobSimulationCalculator":
        """Cast to another type.

        Returns:
            _Cast_HobSimulationCalculator
        """
        return _Cast_HobSimulationCalculator(self)
