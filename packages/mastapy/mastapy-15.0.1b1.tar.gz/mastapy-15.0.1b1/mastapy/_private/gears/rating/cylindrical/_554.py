"""CylindricalGearSetDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _453

_CYLINDRICAL_GEAR_SET_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalGearSetDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1337
    from mastapy._private.gears.gear_designs.cylindrical import _1138
    from mastapy._private.gears.rating import _445
    from mastapy._private.gears.rating.cylindrical import _557, _571
    from mastapy._private.gears.rating.cylindrical.optimisation import _592

    Self = TypeVar("Self", bound="CylindricalGearSetDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetDutyCycleRating._Cast_CylindricalGearSetDutyCycleRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetDutyCycleRating:
    """Special nested class for casting CylindricalGearSetDutyCycleRating to subclasses."""

    __parent__: "CylindricalGearSetDutyCycleRating"

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
    def reduced_cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_571.ReducedCylindricalGearSetDutyCycleRating":
        return self.__parent__._cast(_571.ReducedCylindricalGearSetDutyCycleRating)

    @property
    def cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "CylindricalGearSetDutyCycleRating":
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
class CylindricalGearSetDutyCycleRating(_453.GearSetDutyCycleRating):
    """CylindricalGearSetDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cylindrical_gear_set(self: "Self") -> "_1138.CylindricalGearSetDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def optimisations(
        self: "Self",
    ) -> "_592.CylindricalGearSetRatingOptimisationHelper":
        """mastapy.gears.rating.cylindrical.optimisation.CylindricalGearSetRatingOptimisationHelper

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Optimisations")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def reduced_equivalent_duty_cycle(
        self: "Self",
    ) -> "_571.ReducedCylindricalGearSetDutyCycleRating":
        """mastapy.gears.rating.cylindrical.ReducedCylindricalGearSetDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReducedEquivalentDutyCycle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_mesh_duty_cycle_ratings(
        self: "Self",
    ) -> "List[_557.CylindricalMeshDutyCycleRating]":
        """List[mastapy.gears.rating.cylindrical.CylindricalMeshDutyCycleRating]

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
    def cylindrical_mesh_duty_cycle_ratings(
        self: "Self",
    ) -> "List[_557.CylindricalMeshDutyCycleRating]":
        """List[mastapy.gears.rating.cylindrical.CylindricalMeshDutyCycleRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalMeshDutyCycleRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def quick_optimise_for_safety_factor_and_contact_ratio_with_face_width(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "QuickOptimiseForSafetyFactorAndContactRatioWithFaceWidth"
        )

    @exception_bridge
    def set_profile_shift_to_maximum_safety_factor_fatigue_and_static(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "SetProfileShiftToMaximumSafetyFactorFatigueAndStatic"
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetDutyCycleRating
        """
        return _Cast_CylindricalGearSetDutyCycleRating(self)
