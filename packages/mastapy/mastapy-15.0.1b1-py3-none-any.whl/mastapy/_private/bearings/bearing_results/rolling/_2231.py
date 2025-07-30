"""LoadedNonBarrelRollerBearingDutyCycle"""

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
from mastapy._private.bearings.bearing_results import _2165

_LOADED_NON_BARREL_ROLLER_BEARING_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedNonBarrelRollerBearingDutyCycle",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2154, _2162
    from mastapy._private.bearings.bearing_results.rolling import _2200, _2215, _2254

    Self = TypeVar("Self", bound="LoadedNonBarrelRollerBearingDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedNonBarrelRollerBearingDutyCycle._Cast_LoadedNonBarrelRollerBearingDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedNonBarrelRollerBearingDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedNonBarrelRollerBearingDutyCycle:
    """Special nested class for casting LoadedNonBarrelRollerBearingDutyCycle to subclasses."""

    __parent__: "LoadedNonBarrelRollerBearingDutyCycle"

    @property
    def loaded_rolling_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2165.LoadedRollingBearingDutyCycle":
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
    def loaded_axial_thrust_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2200.LoadedAxialThrustCylindricalRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2200

        return self.__parent__._cast(
            _2200.LoadedAxialThrustCylindricalRollerBearingDutyCycle
        )

    @property
    def loaded_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2215.LoadedCylindricalRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2215

        return self.__parent__._cast(_2215.LoadedCylindricalRollerBearingDutyCycle)

    @property
    def loaded_taper_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2254.LoadedTaperRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2254

        return self.__parent__._cast(_2254.LoadedTaperRollerBearingDutyCycle)

    @property
    def loaded_non_barrel_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "LoadedNonBarrelRollerBearingDutyCycle":
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
class LoadedNonBarrelRollerBearingDutyCycle(_2165.LoadedRollingBearingDutyCycle):
    """LoadedNonBarrelRollerBearingDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_NON_BARREL_ROLLER_BEARING_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def smt_rib_stress_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SMTRibStressSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedNonBarrelRollerBearingDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_LoadedNonBarrelRollerBearingDutyCycle
        """
        return _Cast_LoadedNonBarrelRollerBearingDutyCycle(self)
