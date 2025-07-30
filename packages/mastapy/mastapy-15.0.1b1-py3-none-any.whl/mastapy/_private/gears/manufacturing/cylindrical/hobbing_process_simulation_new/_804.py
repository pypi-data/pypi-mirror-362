"""WormGrindingProcessSimulationViewModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _790,
    _803,
)

_WORM_GRINDING_PROCESS_SIMULATION_VIEW_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "WormGrindingProcessSimulationViewModel",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical import _731

    Self = TypeVar("Self", bound="WormGrindingProcessSimulationViewModel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGrindingProcessSimulationViewModel._Cast_WormGrindingProcessSimulationViewModel",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGrindingProcessSimulationViewModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGrindingProcessSimulationViewModel:
    """Special nested class for casting WormGrindingProcessSimulationViewModel to subclasses."""

    __parent__: "WormGrindingProcessSimulationViewModel"

    @property
    def process_simulation_view_model(
        self: "CastSelf",
    ) -> "_790.ProcessSimulationViewModel":
        return self.__parent__._cast(_790.ProcessSimulationViewModel)

    @property
    def gear_manufacturing_configuration_view_model(
        self: "CastSelf",
    ) -> "_731.GearManufacturingConfigurationViewModel":
        from mastapy._private.gears.manufacturing.cylindrical import _731

        return self.__parent__._cast(_731.GearManufacturingConfigurationViewModel)

    @property
    def worm_grinding_process_simulation_view_model(
        self: "CastSelf",
    ) -> "WormGrindingProcessSimulationViewModel":
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
class WormGrindingProcessSimulationViewModel(
    _790.ProcessSimulationViewModel[_803.WormGrindingProcessSimulationNew]
):
    """WormGrindingProcessSimulationViewModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GRINDING_PROCESS_SIMULATION_VIEW_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_WormGrindingProcessSimulationViewModel":
        """Cast to another type.

        Returns:
            _Cast_WormGrindingProcessSimulationViewModel
        """
        return _Cast_WormGrindingProcessSimulationViewModel(self)
