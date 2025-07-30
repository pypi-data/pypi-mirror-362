"""WormGrindingProcessCalculation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _783,
)

_WORM_GRINDING_PROCESS_CALCULATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "WormGrindingProcessCalculation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _795,
        _796,
        _798,
        _799,
        _800,
        _801,
        _805,
    )

    Self = TypeVar("Self", bound="WormGrindingProcessCalculation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGrindingProcessCalculation._Cast_WormGrindingProcessCalculation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGrindingProcessCalculation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGrindingProcessCalculation:
    """Special nested class for casting WormGrindingProcessCalculation to subclasses."""

    __parent__: "WormGrindingProcessCalculation"

    @property
    def process_calculation(self: "CastSelf") -> "_783.ProcessCalculation":
        return self.__parent__._cast(_783.ProcessCalculation)

    @property
    def worm_grinding_cutter_calculation(
        self: "CastSelf",
    ) -> "_795.WormGrindingCutterCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _795,
        )

        return self.__parent__._cast(_795.WormGrindingCutterCalculation)

    @property
    def worm_grinding_lead_calculation(
        self: "CastSelf",
    ) -> "_796.WormGrindingLeadCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _796,
        )

        return self.__parent__._cast(_796.WormGrindingLeadCalculation)

    @property
    def worm_grinding_process_gear_shape(
        self: "CastSelf",
    ) -> "_798.WormGrindingProcessGearShape":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _798,
        )

        return self.__parent__._cast(_798.WormGrindingProcessGearShape)

    @property
    def worm_grinding_process_mark_on_shaft(
        self: "CastSelf",
    ) -> "_799.WormGrindingProcessMarkOnShaft":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _799,
        )

        return self.__parent__._cast(_799.WormGrindingProcessMarkOnShaft)

    @property
    def worm_grinding_process_pitch_calculation(
        self: "CastSelf",
    ) -> "_800.WormGrindingProcessPitchCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _800,
        )

        return self.__parent__._cast(_800.WormGrindingProcessPitchCalculation)

    @property
    def worm_grinding_process_profile_calculation(
        self: "CastSelf",
    ) -> "_801.WormGrindingProcessProfileCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _801,
        )

        return self.__parent__._cast(_801.WormGrindingProcessProfileCalculation)

    @property
    def worm_grinding_process_total_modification_calculation(
        self: "CastSelf",
    ) -> "_805.WormGrindingProcessTotalModificationCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _805,
        )

        return self.__parent__._cast(
            _805.WormGrindingProcessTotalModificationCalculation
        )

    @property
    def worm_grinding_process_calculation(
        self: "CastSelf",
    ) -> "WormGrindingProcessCalculation":
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
class WormGrindingProcessCalculation(_783.ProcessCalculation):
    """WormGrindingProcessCalculation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GRINDING_PROCESS_CALCULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_WormGrindingProcessCalculation":
        """Cast to another type.

        Returns:
            _Cast_WormGrindingProcessCalculation
        """
        return _Cast_WormGrindingProcessCalculation(self)
