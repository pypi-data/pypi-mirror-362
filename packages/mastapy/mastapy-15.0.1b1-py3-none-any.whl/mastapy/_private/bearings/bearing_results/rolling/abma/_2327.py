"""ANSIABMAResults"""

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

_ANSIABMA_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.ABMA", "ANSIABMAResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.abma import _2325, _2326

    Self = TypeVar("Self", bound="ANSIABMAResults")
    CastSelf = TypeVar("CastSelf", bound="ANSIABMAResults._Cast_ANSIABMAResults")


__docformat__ = "restructuredtext en"
__all__ = ("ANSIABMAResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ANSIABMAResults:
    """Special nested class for casting ANSIABMAResults to subclasses."""

    __parent__: "ANSIABMAResults"

    @property
    def iso_results(self: "CastSelf") -> "_2315.ISOResults":
        return self.__parent__._cast(_2315.ISOResults)

    @property
    def ansiabma112014_results(self: "CastSelf") -> "_2325.ANSIABMA112014Results":
        from mastapy._private.bearings.bearing_results.rolling.abma import _2325

        return self.__parent__._cast(_2325.ANSIABMA112014Results)

    @property
    def ansiabma92015_results(self: "CastSelf") -> "_2326.ANSIABMA92015Results":
        from mastapy._private.bearings.bearing_results.rolling.abma import _2326

        return self.__parent__._cast(_2326.ANSIABMA92015Results)

    @property
    def ansiabma_results(self: "CastSelf") -> "ANSIABMAResults":
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
class ANSIABMAResults(_2315.ISOResults):
    """ANSIABMAResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ANSIABMA_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def e_limiting_value_for_dynamic_equivalent_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ELimitingValueForDynamicEquivalentLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def adjusted_rating_life_cycles(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustedRatingLifeCycles")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def adjusted_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustedRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def adjusted_rating_life_damage_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustedRatingLifeDamageRate")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def adjusted_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustedRatingLifeReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def adjusted_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustedRatingLifeSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def adjusted_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustedRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def adjusted_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustedRatingLifeUnreliability")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def axial_to_radial_load_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialToRadialLoadRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_rating_life_cycles(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRatingLifeCycles")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_rating_life_damage_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRatingLifeDamageRate")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRatingLifeReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRatingLifeSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRatingLifeUnreliability")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bearing_life_adjustment_factor_for_operating_conditions(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BearingLifeAdjustmentFactorForOperatingConditions"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bearing_life_adjustment_factor_for_special_bearing_properties(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BearingLifeAdjustmentFactorForSpecialBearingProperties"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_axial_load_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicAxialLoadFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_equivalent_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicEquivalentLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_radial_load_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicRadialLoadFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def static_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ANSIABMAResults":
        """Cast to another type.

        Returns:
            _Cast_ANSIABMAResults
        """
        return _Cast_ANSIABMAResults(self)
