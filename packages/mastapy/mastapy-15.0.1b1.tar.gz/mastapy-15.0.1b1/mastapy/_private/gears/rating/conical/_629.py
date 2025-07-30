"""ConicalGearDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _448

_CONICAL_GEAR_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Conical", "ConicalGearDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1335
    from mastapy._private.gears.rating import _444, _449
    from mastapy._private.gears.rating.conical import _631, _632

    Self = TypeVar("Self", bound="ConicalGearDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearDutyCycleRating._Cast_ConicalGearDutyCycleRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearDutyCycleRating:
    """Special nested class for casting ConicalGearDutyCycleRating to subclasses."""

    __parent__: "ConicalGearDutyCycleRating"

    @property
    def gear_duty_cycle_rating(self: "CastSelf") -> "_448.GearDutyCycleRating":
        return self.__parent__._cast(_448.GearDutyCycleRating)

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_444.AbstractGearRating":
        from mastapy._private.gears.rating import _444

        return self.__parent__._cast(_444.AbstractGearRating)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def conical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "ConicalGearDutyCycleRating":
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
class ConicalGearDutyCycleRating(_448.GearDutyCycleRating):
    """ConicalGearDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def left_flank_rating(self: "Self") -> "_449.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def concave_flank_rating(self: "Self") -> "_449.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConcaveFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_set_design_duty_cycle(
        self: "Self",
    ) -> "_632.ConicalGearSetDutyCycleRating":
        """mastapy.gears.rating.conical.ConicalGearSetDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetDesignDutyCycle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def conical_gear_set_design_duty_cycle(
        self: "Self",
    ) -> "_632.ConicalGearSetDutyCycleRating":
        """mastapy.gears.rating.conical.ConicalGearSetDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDesignDutyCycle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank_rating(self: "Self") -> "_449.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def convex_flank_rating(self: "Self") -> "_449.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConvexFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_ratings(self: "Self") -> "List[_631.ConicalGearRating]":
        """List[mastapy.gears.rating.conical.ConicalGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def conical_gear_ratings(self: "Self") -> "List[_631.ConicalGearRating]":
        """List[mastapy.gears.rating.conical.ConicalGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearDutyCycleRating
        """
        return _Cast_ConicalGearDutyCycleRating(self)
