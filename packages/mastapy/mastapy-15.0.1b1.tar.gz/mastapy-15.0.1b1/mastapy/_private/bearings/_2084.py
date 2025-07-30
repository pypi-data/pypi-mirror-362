"""BearingSettingsItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings import _2087
from mastapy._private.utility.databases import _2028

_BEARING_SETTINGS_ITEM = python_net_import(
    "SMT.MastaAPI.Bearings", "BearingSettingsItem"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings import _2086, _2093

    Self = TypeVar("Self", bound="BearingSettingsItem")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingSettingsItem._Cast_BearingSettingsItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingSettingsItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingSettingsItem:
    """Special nested class for casting BearingSettingsItem to subclasses."""

    __parent__: "BearingSettingsItem"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def bearing_settings_item(self: "CastSelf") -> "BearingSettingsItem":
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
class BearingSettingsItem(_2028.NamedDatabaseItem):
    """BearingSettingsItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_SETTINGS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ball_bearing_weibull_reliability_slope(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "BallBearingWeibullReliabilitySlope"
        )

        if temp is None:
            return 0.0

        return temp

    @ball_bearing_weibull_reliability_slope.setter
    @exception_bridge
    @enforce_parameter_types
    def ball_bearing_weibull_reliability_slope(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BallBearingWeibullReliabilitySlope",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def failure_probability_for_rating_life_percent(self: "Self") -> "_2093.RatingLife":
        """mastapy.bearings.RatingLife"""
        temp = pythonnet_property_get(
            self.wrapped, "FailureProbabilityForRatingLifePercent"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.RatingLife")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2093", "RatingLife"
        )(value)

    @failure_probability_for_rating_life_percent.setter
    @exception_bridge
    @enforce_parameter_types
    def failure_probability_for_rating_life_percent(
        self: "Self", value: "_2093.RatingLife"
    ) -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Bearings.RatingLife")
        pythonnet_property_set(
            self.wrapped, "FailureProbabilityForRatingLifePercent", value
        )

    @property
    @exception_bridge
    def include_exponent_and_reduction_factors_in_iso162812025(
        self: "Self",
    ) -> "_2086.ExponentAndReductionFactorsInISO16281Calculation":
        """mastapy.bearings.ExponentAndReductionFactorsInISO16281Calculation"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeExponentAndReductionFactorsInISO162812025"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Bearings.ExponentAndReductionFactorsInISO16281Calculation",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2086",
            "ExponentAndReductionFactorsInISO16281Calculation",
        )(value)

    @include_exponent_and_reduction_factors_in_iso162812025.setter
    @exception_bridge
    @enforce_parameter_types
    def include_exponent_and_reduction_factors_in_iso162812025(
        self: "Self", value: "_2086.ExponentAndReductionFactorsInISO16281Calculation"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Bearings.ExponentAndReductionFactorsInISO16281Calculation",
        )
        pythonnet_property_set(
            self.wrapped, "IncludeExponentAndReductionFactorsInISO162812025", value
        )

    @property
    @exception_bridge
    def lubricant_film_temperature_calculation_pressure_fed_grease_filled_bearings(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions":
        """EnumWithSelectedValue[mastapy.bearings.FluidFilmTemperatureOptions]"""
        temp = pythonnet_property_get(
            self.wrapped,
            "LubricantFilmTemperatureCalculationPressureFedGreaseFilledBearings",
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @lubricant_film_temperature_calculation_pressure_fed_grease_filled_bearings.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_film_temperature_calculation_pressure_fed_grease_filled_bearings(
        self: "Self", value: "_2087.FluidFilmTemperatureOptions"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped,
            "LubricantFilmTemperatureCalculationPressureFedGreaseFilledBearings",
            value,
        )

    @property
    @exception_bridge
    def lubricant_film_temperature_calculation_splashed_submerged_bearings(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions":
        """EnumWithSelectedValue[mastapy.bearings.FluidFilmTemperatureOptions]"""
        temp = pythonnet_property_get(
            self.wrapped, "LubricantFilmTemperatureCalculationSplashedSubmergedBearings"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @lubricant_film_temperature_calculation_splashed_submerged_bearings.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_film_temperature_calculation_splashed_submerged_bearings(
        self: "Self", value: "_2087.FluidFilmTemperatureOptions"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped,
            "LubricantFilmTemperatureCalculationSplashedSubmergedBearings",
            value,
        )

    @property
    @exception_bridge
    def number_of_strips_for_roller_calculation(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfStripsForRollerCalculation"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_strips_for_roller_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_strips_for_roller_calculation(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "NumberOfStripsForRollerCalculation", value
        )

    @property
    @exception_bridge
    def roller_bearing_weibull_reliability_slope(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RollerBearingWeibullReliabilitySlope"
        )

        if temp is None:
            return 0.0

        return temp

    @roller_bearing_weibull_reliability_slope.setter
    @exception_bridge
    @enforce_parameter_types
    def roller_bearing_weibull_reliability_slope(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RollerBearingWeibullReliabilitySlope",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def third_weibull_parameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ThirdWeibullParameter")

        if temp is None:
            return 0.0

        return temp

    @third_weibull_parameter.setter
    @exception_bridge
    @enforce_parameter_types
    def third_weibull_parameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ThirdWeibullParameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tolerance_used_for_diameter_warnings_and_database_filter(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ToleranceUsedForDiameterWarningsAndDatabaseFilter"
        )

        if temp is None:
            return 0.0

        return temp

    @tolerance_used_for_diameter_warnings_and_database_filter.setter
    @exception_bridge
    @enforce_parameter_types
    def tolerance_used_for_diameter_warnings_and_database_filter(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceUsedForDiameterWarningsAndDatabaseFilter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_plain_journal_bearing_misalignment_factors(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UsePlainJournalBearingMisalignmentFactors"
        )

        if temp is None:
            return False

        return temp

    @use_plain_journal_bearing_misalignment_factors.setter
    @exception_bridge
    @enforce_parameter_types
    def use_plain_journal_bearing_misalignment_factors(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UsePlainJournalBearingMisalignmentFactors",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BearingSettingsItem":
        """Cast to another type.

        Returns:
            _Cast_BearingSettingsItem
        """
        return _Cast_BearingSettingsItem(self)
