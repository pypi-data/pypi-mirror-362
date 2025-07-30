"""ProcessSimulationViewModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical import _731

_PROCESS_SIMULATION_VIEW_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "ProcessSimulationViewModel",
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _777,
        _804,
    )

    Self = TypeVar("Self", bound="ProcessSimulationViewModel")
    CastSelf = TypeVar(
        "CastSelf", bound="ProcessSimulationViewModel._Cast_ProcessSimulationViewModel"
    )

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("ProcessSimulationViewModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProcessSimulationViewModel:
    """Special nested class for casting ProcessSimulationViewModel to subclasses."""

    __parent__: "ProcessSimulationViewModel"

    @property
    def gear_manufacturing_configuration_view_model(
        self: "CastSelf",
    ) -> "_731.GearManufacturingConfigurationViewModel":
        return self.__parent__._cast(_731.GearManufacturingConfigurationViewModel)

    @property
    def hobbing_process_simulation_view_model(
        self: "CastSelf",
    ) -> "_777.HobbingProcessSimulationViewModel":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _777,
        )

        return self.__parent__._cast(_777.HobbingProcessSimulationViewModel)

    @property
    def worm_grinding_process_simulation_view_model(
        self: "CastSelf",
    ) -> "_804.WormGrindingProcessSimulationViewModel":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _804,
        )

        return self.__parent__._cast(_804.WormGrindingProcessSimulationViewModel)

    @property
    def process_simulation_view_model(self: "CastSelf") -> "ProcessSimulationViewModel":
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
class ProcessSimulationViewModel(
    _731.GearManufacturingConfigurationViewModel, Generic[T]
):
    """ProcessSimulationViewModel

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _PROCESS_SIMULATION_VIEW_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ProcessSimulationViewModel":
        """Cast to another type.

        Returns:
            _Cast_ProcessSimulationViewModel
        """
        return _Cast_ProcessSimulationViewModel(self)
