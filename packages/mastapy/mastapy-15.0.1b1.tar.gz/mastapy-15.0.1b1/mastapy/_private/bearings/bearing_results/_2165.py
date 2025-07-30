"""LoadedRollingBearingDutyCycle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings import _2078
from mastapy._private.bearings.bearing_results import _2162

_LOADED_ROLLING_BEARING_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedRollingBearingDutyCycle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2154
    from mastapy._private.bearings.bearing_results.rolling import (
        _2200,
        _2207,
        _2215,
        _2231,
        _2254,
        _2269,
    )
    from mastapy._private.nodal_analysis import _53
    from mastapy._private.utility.property import _2041, _2042, _2043, _2044

    Self = TypeVar("Self", bound="LoadedRollingBearingDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedRollingBearingDutyCycle._Cast_LoadedRollingBearingDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedRollingBearingDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedRollingBearingDutyCycle:
    """Special nested class for casting LoadedRollingBearingDutyCycle to subclasses."""

    __parent__: "LoadedRollingBearingDutyCycle"

    @property
    def loaded_non_linear_bearing_duty_cycle_results(
        self: "CastSelf",
    ) -> "_2162.LoadedNonLinearBearingDutyCycleResults":
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
    def loaded_ball_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2207.LoadedBallBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2207

        return self.__parent__._cast(_2207.LoadedBallBearingDutyCycle)

    @property
    def loaded_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2215.LoadedCylindricalRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2215

        return self.__parent__._cast(_2215.LoadedCylindricalRollerBearingDutyCycle)

    @property
    def loaded_non_barrel_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2231.LoadedNonBarrelRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2231

        return self.__parent__._cast(_2231.LoadedNonBarrelRollerBearingDutyCycle)

    @property
    def loaded_taper_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2254.LoadedTaperRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2254

        return self.__parent__._cast(_2254.LoadedTaperRollerBearingDutyCycle)

    @property
    def loaded_rolling_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "LoadedRollingBearingDutyCycle":
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
class LoadedRollingBearingDutyCycle(_2162.LoadedNonLinearBearingDutyCycleResults):
    """LoadedRollingBearingDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ROLLING_BEARING_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ansiabma_adjusted_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMAAdjustedRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ansiabma_adjusted_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMAAdjustedRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ansiabma_adjusted_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMAAdjustedRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ansiabma_adjusted_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMAAdjustedRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ansiabma_adjusted_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMAAdjustedRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ansiabma_basic_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMABasicRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ansiabma_basic_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMABasicRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ansiabma_basic_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMABasicRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ansiabma_basic_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMABasicRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ansiabma_basic_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMABasicRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ansiabma_dynamic_equivalent_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMADynamicEquivalentLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso162812025_basic_reference_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO162812025BasicReferenceRatingLifeDamage"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso162812025_basic_reference_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO162812025BasicReferenceRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso162812025_basic_reference_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO162812025BasicReferenceRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso162812025_basic_reference_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO162812025BasicReferenceRatingLifeTime"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso162812025_basic_reference_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO162812025BasicReferenceRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso162812025_dynamic_equivalent_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO162812025DynamicEquivalentLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso162812025_modified_reference_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO162812025ModifiedReferenceRatingLifeDamage"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso162812025_modified_reference_rating_life_reliability(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO162812025ModifiedReferenceRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso162812025_modified_reference_rating_life_safety_factor(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO162812025ModifiedReferenceRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso162812025_modified_reference_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO162812025ModifiedReferenceRatingLifeTime"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso162812025_modified_reference_rating_life_unreliability(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO162812025ModifiedReferenceRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso2812007_basic_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO2812007BasicRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso2812007_basic_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007BasicRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso2812007_basic_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007BasicRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso2812007_basic_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO2812007BasicRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso2812007_basic_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007BasicRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso2812007_dynamic_equivalent_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO2812007DynamicEquivalentLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso2812007_modified_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007ModifiedRatingLifeDamage"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso2812007_modified_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007ModifiedRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso2812007_modified_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007ModifiedRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso2812007_modified_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO2812007ModifiedRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso2812007_modified_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007ModifiedRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso762006_recommended_maximum_element_normal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO762006RecommendedMaximumElementNormalStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lambda_ratio_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LambdaRatioInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lambda_ratio_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LambdaRatioOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_element_normal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumElementNormalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lambda_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumLambdaRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lubricating_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumLubricatingFilmThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lubricating_film_thickness_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lubricating_film_thickness_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def skf_bearing_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFBearingRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def skf_bearing_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFBearingRatingLifeReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def skf_bearing_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFBearingRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def skf_bearing_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFBearingRatingLifeUnreliability")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def static_equivalent_load_capacity_ratio_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StaticEquivalentLoadCapacityRatioLimit"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_ansiabma_static_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstANSIABMAStaticSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_iso762006_safety_factor_static_equivalent_load_capacity_ratio(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstISO762006SafetyFactorStaticEquivalentLoadCapacityRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ansiabma_dynamic_equivalent_load_summary(
        self: "Self",
    ) -> "_2041.DutyCyclePropertySummaryForce[_2078.BearingLoadCaseResultsLightweight]":
        """mastapy.utility.property.DutyCyclePropertySummaryForce[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMADynamicEquivalentLoadSummary"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _2078.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    @exception_bridge
    def analysis_settings(self: "Self") -> "_53.AnalysisSettingsItem":
        """mastapy.nodal_analysis.AnalysisSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def iso162812025_dynamic_equivalent_load_summary(
        self: "Self",
    ) -> "_2041.DutyCyclePropertySummaryForce[_2078.BearingLoadCaseResultsLightweight]":
        """mastapy.utility.property.DutyCyclePropertySummaryForce[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO162812025DynamicEquivalentLoadSummary"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _2078.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    @exception_bridge
    def iso2812007_dynamic_equivalent_load_summary(
        self: "Self",
    ) -> "_2041.DutyCyclePropertySummaryForce[_2078.BearingLoadCaseResultsLightweight]":
        """mastapy.utility.property.DutyCyclePropertySummaryForce[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007DynamicEquivalentLoadSummary"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _2078.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    @exception_bridge
    def maximum_element_normal_stress_inner_summary(
        self: "Self",
    ) -> (
        "_2044.DutyCyclePropertySummaryStress[_2078.BearingLoadCaseResultsLightweight]"
    ):
        """mastapy.utility.property.DutyCyclePropertySummaryStress[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumElementNormalStressInnerSummary"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _2078.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    @exception_bridge
    def maximum_element_normal_stress_outer_summary(
        self: "Self",
    ) -> (
        "_2044.DutyCyclePropertySummaryStress[_2078.BearingLoadCaseResultsLightweight]"
    ):
        """mastapy.utility.property.DutyCyclePropertySummaryStress[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumElementNormalStressOuterSummary"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _2078.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    @exception_bridge
    def maximum_element_normal_stress_summary(
        self: "Self",
    ) -> (
        "_2044.DutyCyclePropertySummaryStress[_2078.BearingLoadCaseResultsLightweight]"
    ):
        """mastapy.utility.property.DutyCyclePropertySummaryStress[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumElementNormalStressSummary")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _2078.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    @exception_bridge
    def maximum_static_contact_stress_duty_cycle(
        self: "Self",
    ) -> "_2269.MaximumStaticContactStressDutyCycle":
        """mastapy.bearings.bearing_results.rolling.MaximumStaticContactStressDutyCycle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumStaticContactStressDutyCycle"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def maximum_truncation_summary(
        self: "Self",
    ) -> "_2042.DutyCyclePropertySummaryPercentage[_2078.BearingLoadCaseResultsLightweight]":
        """mastapy.utility.property.DutyCyclePropertySummaryPercentage[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumTruncationSummary")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _2078.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    @exception_bridge
    def misalignment_summary(
        self: "Self",
    ) -> "_2043.DutyCyclePropertySummarySmallAngle[_2078.BearingLoadCaseResultsLightweight]":
        """mastapy.utility.property.DutyCyclePropertySummarySmallAngle[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentSummary")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _2078.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedRollingBearingDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_LoadedRollingBearingDutyCycle
        """
        return _Cast_LoadedRollingBearingDutyCycle(self)
