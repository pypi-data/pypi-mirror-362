"""WormGrindingProcessSimulationInput"""

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
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _788,
)

_WORM_GRINDING_PROCESS_SIMULATION_INPUT = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "WormGrindingProcessSimulationInput",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _794,
    )

    Self = TypeVar("Self", bound="WormGrindingProcessSimulationInput")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGrindingProcessSimulationInput._Cast_WormGrindingProcessSimulationInput",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGrindingProcessSimulationInput",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGrindingProcessSimulationInput:
    """Special nested class for casting WormGrindingProcessSimulationInput to subclasses."""

    __parent__: "WormGrindingProcessSimulationInput"

    @property
    def process_simulation_input(self: "CastSelf") -> "_788.ProcessSimulationInput":
        return self.__parent__._cast(_788.ProcessSimulationInput)

    @property
    def worm_grinding_process_simulation_input(
        self: "CastSelf",
    ) -> "WormGrindingProcessSimulationInput":
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
class WormGrindingProcessSimulationInput(_788.ProcessSimulationInput):
    """WormGrindingProcessSimulationInput

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GRINDING_PROCESS_SIMULATION_INPUT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def worm_grinder_manufacture_error(
        self: "Self",
    ) -> "_794.WormGrinderManufactureError":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.WormGrinderManufactureError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGrinderManufactureError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_WormGrindingProcessSimulationInput":
        """Cast to another type.

        Returns:
            _Cast_WormGrindingProcessSimulationInput
        """
        return _Cast_WormGrindingProcessSimulationInput(self)
