"""InterferenceFitDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_INTERFERENCE_FIT_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits.DutyCycleRatings",
    "InterferenceFitDutyCycleRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InterferenceFitDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterferenceFitDutyCycleRating._Cast_InterferenceFitDutyCycleRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterferenceFitDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterferenceFitDutyCycleRating:
    """Special nested class for casting InterferenceFitDutyCycleRating to subclasses."""

    __parent__: "InterferenceFitDutyCycleRating"

    @property
    def interference_fit_duty_cycle_rating(
        self: "CastSelf",
    ) -> "InterferenceFitDutyCycleRating":
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
class InterferenceFitDutyCycleRating(_0.APIBase):
    """InterferenceFitDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTERFERENCE_FIT_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def safety_factor_for_axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForAxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_InterferenceFitDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_InterferenceFitDutyCycleRating
        """
        return _Cast_InterferenceFitDutyCycleRating(self)
