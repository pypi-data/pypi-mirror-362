"""WormGrinderSimulationCalculator"""

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

_WORM_GRINDER_SIMULATION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "WormGrinderSimulationCalculator",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _834
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _831

    Self = TypeVar("Self", bound="WormGrinderSimulationCalculator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGrinderSimulationCalculator._Cast_WormGrinderSimulationCalculator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGrinderSimulationCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGrinderSimulationCalculator:
    """Special nested class for casting WormGrinderSimulationCalculator to subclasses."""

    __parent__: "WormGrinderSimulationCalculator"

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
    def worm_grinder_simulation_calculator(
        self: "CastSelf",
    ) -> "WormGrinderSimulationCalculator":
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
class WormGrinderSimulationCalculator(_846.RackSimulationCalculator):
    """WormGrinderSimulationCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GRINDER_SIMULATION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def worm_grinder(self: "Self") -> "_831.CylindricalGearWormGrinderShape":
        """mastapy.gears.manufacturing.cylindrical.cutters.tangibles.CylindricalGearWormGrinderShape

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGrinder")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_WormGrinderSimulationCalculator":
        """Cast to another type.

        Returns:
            _Cast_WormGrinderSimulationCalculator
        """
        return _Cast_WormGrinderSimulationCalculator(self)
