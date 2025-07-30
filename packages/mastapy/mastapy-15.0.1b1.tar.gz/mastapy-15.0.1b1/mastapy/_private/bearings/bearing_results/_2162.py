"""LoadedNonLinearBearingDutyCycleResults"""

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
from mastapy._private.bearings.bearing_results import _2154

_LOADED_NON_LINEAR_BEARING_DUTY_CYCLE_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedNonLinearBearingDutyCycleResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2165
    from mastapy._private.bearings.bearing_results.rolling import (
        _2200,
        _2207,
        _2215,
        _2231,
        _2254,
    )

    Self = TypeVar("Self", bound="LoadedNonLinearBearingDutyCycleResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedNonLinearBearingDutyCycleResults._Cast_LoadedNonLinearBearingDutyCycleResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedNonLinearBearingDutyCycleResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedNonLinearBearingDutyCycleResults:
    """Special nested class for casting LoadedNonLinearBearingDutyCycleResults to subclasses."""

    __parent__: "LoadedNonLinearBearingDutyCycleResults"

    @property
    def loaded_bearing_duty_cycle(self: "CastSelf") -> "_2154.LoadedBearingDutyCycle":
        return self.__parent__._cast(_2154.LoadedBearingDutyCycle)

    @property
    def loaded_rolling_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2165.LoadedRollingBearingDutyCycle":
        from mastapy._private.bearings.bearing_results import _2165

        return self.__parent__._cast(_2165.LoadedRollingBearingDutyCycle)

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2200.LoadedAxialThrustCylindricalRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2200

        return self.__parent__._cast(
            _2200.LoadedAxialThrustCylindricalRollerBearingDutyCycle
        )

    @property
    def loaded_ball_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2207.LoadedBallBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2207

        return self.__parent__._cast(_2207.LoadedBallBearingDutyCycle)

    @property
    def loaded_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2215.LoadedCylindricalRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2215

        return self.__parent__._cast(_2215.LoadedCylindricalRollerBearingDutyCycle)

    @property
    def loaded_non_barrel_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2231.LoadedNonBarrelRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2231

        return self.__parent__._cast(_2231.LoadedNonBarrelRollerBearingDutyCycle)

    @property
    def loaded_taper_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2254.LoadedTaperRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2254

        return self.__parent__._cast(_2254.LoadedTaperRollerBearingDutyCycle)

    @property
    def loaded_non_linear_bearing_duty_cycle_results(
        self: "CastSelf",
    ) -> "LoadedNonLinearBearingDutyCycleResults":
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
class LoadedNonLinearBearingDutyCycleResults(_2154.LoadedBearingDutyCycle):
    """LoadedNonLinearBearingDutyCycleResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_NON_LINEAR_BEARING_DUTY_CYCLE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def total_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedNonLinearBearingDutyCycleResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedNonLinearBearingDutyCycleResults
        """
        return _Cast_LoadedNonLinearBearingDutyCycleResults(self)
