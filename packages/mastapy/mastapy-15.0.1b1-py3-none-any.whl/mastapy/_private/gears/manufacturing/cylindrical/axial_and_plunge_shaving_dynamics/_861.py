"""PlungeShavingDynamicsCalculationForDesignedGears"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _858,
    _870,
)

_PLUNGE_SHAVING_DYNAMICS_CALCULATION_FOR_DESIGNED_GEARS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "PlungeShavingDynamicsCalculationForDesignedGears",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
        _869,
    )

    Self = TypeVar("Self", bound="PlungeShavingDynamicsCalculationForDesignedGears")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlungeShavingDynamicsCalculationForDesignedGears._Cast_PlungeShavingDynamicsCalculationForDesignedGears",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlungeShavingDynamicsCalculationForDesignedGears",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlungeShavingDynamicsCalculationForDesignedGears:
    """Special nested class for casting PlungeShavingDynamicsCalculationForDesignedGears to subclasses."""

    __parent__: "PlungeShavingDynamicsCalculationForDesignedGears"

    @property
    def shaving_dynamics_calculation_for_designed_gears(
        self: "CastSelf",
    ) -> "_870.ShavingDynamicsCalculationForDesignedGears":
        return self.__parent__._cast(_870.ShavingDynamicsCalculationForDesignedGears)

    @property
    def shaving_dynamics_calculation(
        self: "CastSelf",
    ) -> "_869.ShavingDynamicsCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _869,
        )

        return self.__parent__._cast(_869.ShavingDynamicsCalculation)

    @property
    def plunge_shaving_dynamics_calculation_for_designed_gears(
        self: "CastSelf",
    ) -> "PlungeShavingDynamicsCalculationForDesignedGears":
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
class PlungeShavingDynamicsCalculationForDesignedGears(
    _870.ShavingDynamicsCalculationForDesignedGears[_858.PlungeShaverDynamics]
):
    """PlungeShavingDynamicsCalculationForDesignedGears

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLUNGE_SHAVING_DYNAMICS_CALCULATION_FOR_DESIGNED_GEARS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_PlungeShavingDynamicsCalculationForDesignedGears":
        """Cast to another type.

        Returns:
            _Cast_PlungeShavingDynamicsCalculationForDesignedGears
        """
        return _Cast_PlungeShavingDynamicsCalculationForDesignedGears(self)
