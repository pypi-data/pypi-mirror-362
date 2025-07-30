"""ISO162812025Results"""

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
from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import _2315

_ISO162812025_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults",
    "ISO162812025Results",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
        _2310,
        _2316,
    )

    Self = TypeVar("Self", bound="ISO162812025Results")
    CastSelf = TypeVar(
        "CastSelf", bound="ISO162812025Results._Cast_ISO162812025Results"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO162812025Results",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO162812025Results:
    """Special nested class for casting ISO162812025Results to subclasses."""

    __parent__: "ISO162812025Results"

    @property
    def iso_results(self: "CastSelf") -> "_2315.ISOResults":
        return self.__parent__._cast(_2315.ISOResults)

    @property
    def ball_iso162812025_results(self: "CastSelf") -> "_2310.BallISO162812025Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2310,
        )

        return self.__parent__._cast(_2310.BallISO162812025Results)

    @property
    def roller_iso162812025_results(
        self: "CastSelf",
    ) -> "_2316.RollerISO162812025Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2316,
        )

        return self.__parent__._cast(_2316.RollerISO162812025Results)

    @property
    def iso162812025_results(self: "CastSelf") -> "ISO162812025Results":
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
class ISO162812025Results(_2315.ISOResults):
    """ISO162812025Results

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO162812025_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def basic_reference_rating_life_cycles(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicReferenceRatingLifeCycles")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_reference_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicReferenceRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_reference_rating_life_damage_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BasicReferenceRatingLifeDamageRate"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_reference_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BasicReferenceRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_reference_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BasicReferenceRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_reference_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicReferenceRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_reference_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BasicReferenceRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_equivalent_load_dynamic_capacity_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DynamicEquivalentLoadDynamicCapacityRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_equivalent_reference_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicEquivalentReferenceLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def life_modification_factor_for_systems_approach(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LifeModificationFactorForSystemsApproach"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_for_the_basic_dynamic_load_rating_of_the_inner_ring_or_shaft_washer(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadForTheBasicDynamicLoadRatingOfTheInnerRingOrShaftWasher"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_for_the_basic_dynamic_load_rating_of_the_outer_ring_or_housing_washer(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LoadForTheBasicDynamicLoadRatingOfTheOuterRingOrHousingWasher",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_reference_rating_life_cycles(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedReferenceRatingLifeCycles")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_reference_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedReferenceRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_reference_rating_life_damage_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ModifiedReferenceRatingLifeDamageRate"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_reference_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ModifiedReferenceRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_reference_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ModifiedReferenceRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_reference_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedReferenceRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_reference_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ModifiedReferenceRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO162812025Results":
        """Cast to another type.

        Returns:
            _Cast_ISO162812025Results
        """
        return _Cast_ISO162812025Results(self)
