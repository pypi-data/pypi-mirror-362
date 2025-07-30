"""ISO2812007Results"""

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

_ISO2812007_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults", "ISO2812007Results"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
        _2311,
        _2317,
    )

    Self = TypeVar("Self", bound="ISO2812007Results")
    CastSelf = TypeVar("CastSelf", bound="ISO2812007Results._Cast_ISO2812007Results")


__docformat__ = "restructuredtext en"
__all__ = ("ISO2812007Results",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO2812007Results:
    """Special nested class for casting ISO2812007Results to subclasses."""

    __parent__: "ISO2812007Results"

    @property
    def iso_results(self: "CastSelf") -> "_2315.ISOResults":
        return self.__parent__._cast(_2315.ISOResults)

    @property
    def ball_iso2812007_results(self: "CastSelf") -> "_2311.BallISO2812007Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2311,
        )

        return self.__parent__._cast(_2311.BallISO2812007Results)

    @property
    def roller_iso2812007_results(self: "CastSelf") -> "_2317.RollerISO2812007Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2317,
        )

        return self.__parent__._cast(_2317.RollerISO2812007Results)

    @property
    def iso2812007_results(self: "CastSelf") -> "ISO2812007Results":
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
class ISO2812007Results(_2315.ISOResults):
    """ISO2812007Results

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO2812007_RESULTS

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
    def axial_to_radial_load_ratio_exceeds_iso2812007e_limiting_value_for_dynamic_equivalent_load(
        self: "Self",
    ) -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AxialToRadialLoadRatioExceedsISO2812007ELimitingValueForDynamicEquivalentLoad",
        )

        if temp is None:
            return False

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
    def calculated_viscosity_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedViscosityRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contamination_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContaminationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contamination_factor_from_calculated_viscosity_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContaminationFactorFromCalculatedViscosityRatio"
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
    def life_modification_factor_for_systems_approach_with_calculated_viscosity_ratio(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LifeModificationFactorForSystemsApproachWithCalculatedViscosityRatio",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_rating_life_cycles(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedRatingLifeCycles")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_rating_life_damage_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedRatingLifeDamageRate")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedRatingLifeReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedRatingLifeSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedRatingLifeUnreliability")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reference_kinematic_viscosity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceKinematicViscosity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def viscosity_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ViscosityRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO2812007Results":
        """Cast to another type.

        Returns:
            _Cast_ISO2812007Results
        """
        return _Cast_ISO2812007Results(self)
