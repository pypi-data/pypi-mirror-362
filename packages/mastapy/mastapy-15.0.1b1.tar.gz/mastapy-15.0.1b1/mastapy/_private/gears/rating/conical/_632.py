"""ConicalGearSetDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _453

_CONICAL_GEAR_SET_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Conical", "ConicalGearSetDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1337
    from mastapy._private.gears.rating import _445
    from mastapy._private.gears.rating.conical import _635

    Self = TypeVar("Self", bound="ConicalGearSetDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetDutyCycleRating._Cast_ConicalGearSetDutyCycleRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetDutyCycleRating:
    """Special nested class for casting ConicalGearSetDutyCycleRating to subclasses."""

    __parent__: "ConicalGearSetDutyCycleRating"

    @property
    def gear_set_duty_cycle_rating(self: "CastSelf") -> "_453.GearSetDutyCycleRating":
        return self.__parent__._cast(_453.GearSetDutyCycleRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_445.AbstractGearSetRating":
        from mastapy._private.gears.rating import _445

        return self.__parent__._cast(_445.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1337

        return self.__parent__._cast(_1337.AbstractGearSetAnalysis)

    @property
    def conical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "ConicalGearSetDutyCycleRating":
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
class ConicalGearSetDutyCycleRating(_453.GearSetDutyCycleRating):
    """ConicalGearSetDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_mesh_duty_cycle_ratings(
        self: "Self",
    ) -> "List[_635.ConicalMeshDutyCycleRating]":
        """List[mastapy.gears.rating.conical.ConicalMeshDutyCycleRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshDutyCycleRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def conical_mesh_duty_cycle_ratings(
        self: "Self",
    ) -> "List[_635.ConicalMeshDutyCycleRating]":
        """List[mastapy.gears.rating.conical.ConicalMeshDutyCycleRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshDutyCycleRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetDutyCycleRating
        """
        return _Cast_ConicalGearSetDutyCycleRating(self)
