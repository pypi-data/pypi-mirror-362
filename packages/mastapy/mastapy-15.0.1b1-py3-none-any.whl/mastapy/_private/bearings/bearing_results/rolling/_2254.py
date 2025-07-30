"""LoadedTaperRollerBearingDutyCycle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2231

_LOADED_TAPER_ROLLER_BEARING_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedTaperRollerBearingDutyCycle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2154, _2162, _2165

    Self = TypeVar("Self", bound="LoadedTaperRollerBearingDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedTaperRollerBearingDutyCycle._Cast_LoadedTaperRollerBearingDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedTaperRollerBearingDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedTaperRollerBearingDutyCycle:
    """Special nested class for casting LoadedTaperRollerBearingDutyCycle to subclasses."""

    __parent__: "LoadedTaperRollerBearingDutyCycle"

    @property
    def loaded_non_barrel_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2231.LoadedNonBarrelRollerBearingDutyCycle":
        return self.__parent__._cast(_2231.LoadedNonBarrelRollerBearingDutyCycle)

    @property
    def loaded_rolling_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2165.LoadedRollingBearingDutyCycle":
        from mastapy._private.bearings.bearing_results import _2165

        return self.__parent__._cast(_2165.LoadedRollingBearingDutyCycle)

    @property
    def loaded_non_linear_bearing_duty_cycle_results(
        self: "CastSelf",
    ) -> "_2162.LoadedNonLinearBearingDutyCycleResults":
        from mastapy._private.bearings.bearing_results import _2162

        return self.__parent__._cast(_2162.LoadedNonLinearBearingDutyCycleResults)

    @property
    def loaded_bearing_duty_cycle(self: "CastSelf") -> "_2154.LoadedBearingDutyCycle":
        from mastapy._private.bearings.bearing_results import _2154

        return self.__parent__._cast(_2154.LoadedBearingDutyCycle)

    @property
    def loaded_taper_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "LoadedTaperRollerBearingDutyCycle":
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
class LoadedTaperRollerBearingDutyCycle(_2231.LoadedNonBarrelRollerBearingDutyCycle):
    """LoadedTaperRollerBearingDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_TAPER_ROLLER_BEARING_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedTaperRollerBearingDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_LoadedTaperRollerBearingDutyCycle
        """
        return _Cast_LoadedTaperRollerBearingDutyCycle(self)
