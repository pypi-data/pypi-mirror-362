"""LoadedCylindricalRollerBearingDutyCycle"""

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
from mastapy._private.bearings.bearing_results.rolling import _2231

_LOADED_CYLINDRICAL_ROLLER_BEARING_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedCylindricalRollerBearingDutyCycle",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2154, _2162, _2165

    Self = TypeVar("Self", bound="LoadedCylindricalRollerBearingDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedCylindricalRollerBearingDutyCycle._Cast_LoadedCylindricalRollerBearingDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedCylindricalRollerBearingDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedCylindricalRollerBearingDutyCycle:
    """Special nested class for casting LoadedCylindricalRollerBearingDutyCycle to subclasses."""

    __parent__: "LoadedCylindricalRollerBearingDutyCycle"

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
    def loaded_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "LoadedCylindricalRollerBearingDutyCycle":
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
class LoadedCylindricalRollerBearingDutyCycle(
    _2231.LoadedNonBarrelRollerBearingDutyCycle
):
    """LoadedCylindricalRollerBearingDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_CYLINDRICAL_ROLLER_BEARING_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def permissible_continuous_axial_load_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleContinuousAxialLoadSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedCylindricalRollerBearingDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_LoadedCylindricalRollerBearingDutyCycle
        """
        return _Cast_LoadedCylindricalRollerBearingDutyCycle(self)
