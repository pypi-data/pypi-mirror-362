"""CylindricalGearDesignAndRatingSettingsItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    overridable_enum_runtime,
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
from mastapy._private.gears import _408, _424
from mastapy._private.gears.rating.cylindrical import _572, _573
from mastapy._private.materials import _338
from mastapy._private.utility.databases import _2028

_CYLINDRICAL_GEAR_DESIGN_AND_RATING_SETTINGS_ITEM = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical",
    "CylindricalGearDesignAndRatingSettingsItem",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears import _404, _434
    from mastapy._private.gears.gear_designs.cylindrical import _1136
    from mastapy._private.gears.rating.cylindrical import (
        _563,
        _564,
        _567,
        _570,
        _574,
        _577,
        _578,
    )
    from mastapy._private.utility.units_and_measurements import _1799

    Self = TypeVar("Self", bound="CylindricalGearDesignAndRatingSettingsItem")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearDesignAndRatingSettingsItem._Cast_CylindricalGearDesignAndRatingSettingsItem",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearDesignAndRatingSettingsItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearDesignAndRatingSettingsItem:
    """Special nested class for casting CylindricalGearDesignAndRatingSettingsItem to subclasses."""

    __parent__: "CylindricalGearDesignAndRatingSettingsItem"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def cylindrical_gear_design_and_rating_settings_item(
        self: "CastSelf",
    ) -> "CylindricalGearDesignAndRatingSettingsItem":
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
class CylindricalGearDesignAndRatingSettingsItem(_2028.NamedDatabaseItem):
    """CylindricalGearDesignAndRatingSettingsItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_DESIGN_AND_RATING_SETTINGS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def agma_quality_grade_type(self: "Self") -> "_434.QualityGradeTypes":
        """mastapy.gears.QualityGradeTypes"""
        temp = pythonnet_property_get(self.wrapped, "AGMAQualityGradeType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.QualityGradeTypes")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._434", "QualityGradeTypes"
        )(value)

    @agma_quality_grade_type.setter
    @exception_bridge
    @enforce_parameter_types
    def agma_quality_grade_type(self: "Self", value: "_434.QualityGradeTypes") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Gears.QualityGradeTypes")
        pythonnet_property_set(self.wrapped, "AGMAQualityGradeType", value)

    @property
    @exception_bridge
    def agma_stress_cycle_factor_influence_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AGMAStressCycleFactorInfluenceFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @agma_stress_cycle_factor_influence_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def agma_stress_cycle_factor_influence_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AGMAStressCycleFactorInfluenceFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def agma_tolerances_standard(self: "Self") -> "_404.AGMAToleranceStandard":
        """mastapy.gears.AGMAToleranceStandard"""
        temp = pythonnet_property_get(self.wrapped, "AGMATolerancesStandard")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.AGMAToleranceStandard"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._404", "AGMAToleranceStandard"
        )(value)

    @agma_tolerances_standard.setter
    @exception_bridge
    @enforce_parameter_types
    def agma_tolerances_standard(
        self: "Self", value: "_404.AGMAToleranceStandard"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.AGMAToleranceStandard"
        )
        pythonnet_property_set(self.wrapped, "AGMATolerancesStandard", value)

    @property
    @exception_bridge
    def allow_transverse_contact_ratio_less_than_one(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "AllowTransverseContactRatioLessThanOne"
        )

        if temp is None:
            return False

        return temp

    @allow_transverse_contact_ratio_less_than_one.setter
    @exception_bridge
    @enforce_parameter_types
    def allow_transverse_contact_ratio_less_than_one(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowTransverseContactRatioLessThanOne",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def always_use_chosen_tooth_thickness_for_bending_strength(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "AlwaysUseChosenToothThicknessForBendingStrength"
        )

        if temp is None:
            return False

        return temp

    @always_use_chosen_tooth_thickness_for_bending_strength.setter
    @exception_bridge
    @enforce_parameter_types
    def always_use_chosen_tooth_thickness_for_bending_strength(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AlwaysUseChosenToothThicknessForBendingStrength",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def apply_application_and_dynamic_factor_by_default(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ApplyApplicationAndDynamicFactorByDefault"
        )

        if temp is None:
            return False

        return temp

    @apply_application_and_dynamic_factor_by_default.setter
    @exception_bridge
    @enforce_parameter_types
    def apply_application_and_dynamic_factor_by_default(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ApplyApplicationAndDynamicFactorByDefault",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def apply_work_hardening_factor_for_wrought_normalised_low_carbon_steel_and_cast_steel(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "ApplyWorkHardeningFactorForWroughtNormalisedLowCarbonSteelAndCastSteel",
        )

        if temp is None:
            return False

        return temp

    @apply_work_hardening_factor_for_wrought_normalised_low_carbon_steel_and_cast_steel.setter
    @exception_bridge
    @enforce_parameter_types
    def apply_work_hardening_factor_for_wrought_normalised_low_carbon_steel_and_cast_steel(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ApplyWorkHardeningFactorForWroughtNormalisedLowCarbonSteelAndCastSteel",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def chosen_tooth_thickness_for_bending_strength(
        self: "Self",
    ) -> "_578.ToothThicknesses":
        """mastapy.gears.rating.cylindrical.ToothThicknesses"""
        temp = pythonnet_property_get(
            self.wrapped, "ChosenToothThicknessForBendingStrength"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Cylindrical.ToothThicknesses"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical._578", "ToothThicknesses"
        )(value)

    @chosen_tooth_thickness_for_bending_strength.setter
    @exception_bridge
    @enforce_parameter_types
    def chosen_tooth_thickness_for_bending_strength(
        self: "Self", value: "_578.ToothThicknesses"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Cylindrical.ToothThicknesses"
        )
        pythonnet_property_set(
            self.wrapped, "ChosenToothThicknessForBendingStrength", value
        )

    @property
    @exception_bridge
    def cylindrical_gear_profile_measurement(
        self: "Self",
    ) -> "_1136.CylindricalGearProfileMeasurementType":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurementType"""
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearProfileMeasurement")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CylindricalGearProfileMeasurementType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1136",
            "CylindricalGearProfileMeasurementType",
        )(value)

    @cylindrical_gear_profile_measurement.setter
    @exception_bridge
    @enforce_parameter_types
    def cylindrical_gear_profile_measurement(
        self: "Self", value: "_1136.CylindricalGearProfileMeasurementType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CylindricalGearProfileMeasurementType",
        )
        pythonnet_property_set(self.wrapped, "CylindricalGearProfileMeasurement", value)

    @property
    @exception_bridge
    def default_coefficient_of_friction_calculation_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod":
        """EnumWithSelectedValue[mastapy.gears.CoefficientOfFrictionCalculationMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "DefaultCoefficientOfFrictionCalculationMethod"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @default_coefficient_of_friction_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def default_coefficient_of_friction_calculation_method(
        self: "Self", value: "_408.CoefficientOfFrictionCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "DefaultCoefficientOfFrictionCalculationMethod", value
        )

    @property
    @exception_bridge
    def dynamic_factor_method(self: "Self") -> "_563.DynamicFactorMethods":
        """mastapy.gears.rating.cylindrical.DynamicFactorMethods"""
        temp = pythonnet_property_get(self.wrapped, "DynamicFactorMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Cylindrical.DynamicFactorMethods"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical._563", "DynamicFactorMethods"
        )(value)

    @dynamic_factor_method.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_factor_method(self: "Self", value: "_563.DynamicFactorMethods") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Cylindrical.DynamicFactorMethods"
        )
        pythonnet_property_set(self.wrapped, "DynamicFactorMethod", value)

    @property
    @exception_bridge
    def enable_proportion_system_for_tip_alteration_coefficient(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "EnableProportionSystemForTipAlterationCoefficient"
        )

        if temp is None:
            return False

        return temp

    @enable_proportion_system_for_tip_alteration_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def enable_proportion_system_for_tip_alteration_coefficient(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EnableProportionSystemForTipAlterationCoefficient",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def film_thickness_equation_for_scuffing(self: "Self") -> "_574.ScuffingMethods":
        """mastapy.gears.rating.cylindrical.ScuffingMethods"""
        temp = pythonnet_property_get(self.wrapped, "FilmThicknessEquationForScuffing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Cylindrical.ScuffingMethods"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical._574", "ScuffingMethods"
        )(value)

    @film_thickness_equation_for_scuffing.setter
    @exception_bridge
    @enforce_parameter_types
    def film_thickness_equation_for_scuffing(
        self: "Self", value: "_574.ScuffingMethods"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Cylindrical.ScuffingMethods"
        )
        pythonnet_property_set(self.wrapped, "FilmThicknessEquationForScuffing", value)

    @property
    @exception_bridge
    def gear_blank_factor_calculation_option(
        self: "Self",
    ) -> "_564.GearBlankFactorCalculationOptions":
        """mastapy.gears.rating.cylindrical.GearBlankFactorCalculationOptions"""
        temp = pythonnet_property_get(self.wrapped, "GearBlankFactorCalculationOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Rating.Cylindrical.GearBlankFactorCalculationOptions",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical._564",
            "GearBlankFactorCalculationOptions",
        )(value)

    @gear_blank_factor_calculation_option.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_blank_factor_calculation_option(
        self: "Self", value: "_564.GearBlankFactorCalculationOptions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Rating.Cylindrical.GearBlankFactorCalculationOptions",
        )
        pythonnet_property_set(self.wrapped, "GearBlankFactorCalculationOption", value)

    @property
    @exception_bridge
    def iso_tolerances_standard(
        self: "Self",
    ) -> "overridable.Overridable_ISOToleranceStandard":
        """Overridable[mastapy.gears.ISOToleranceStandard]"""
        temp = pythonnet_property_get(self.wrapped, "ISOTolerancesStandard")

        if temp is None:
            return None

        value = overridable.Overridable_ISOToleranceStandard.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @iso_tolerances_standard.setter
    @exception_bridge
    @enforce_parameter_types
    def iso_tolerances_standard(
        self: "Self",
        value: "Union[_424.ISOToleranceStandard, Tuple[_424.ISOToleranceStandard, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_ISOToleranceStandard.wrapper_type()
        enclosed_type = overridable.Overridable_ISOToleranceStandard.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ISOTolerancesStandard", value)

    @property
    @exception_bridge
    def include_rim_thickness_factor(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeRimThicknessFactor")

        if temp is None:
            return False

        return temp

    @include_rim_thickness_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def include_rim_thickness_factor(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeRimThicknessFactor",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def internal_gear_root_fillet_radius_is_always_equal_to_basic_rack_root_fillet_radius(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "InternalGearRootFilletRadiusIsAlwaysEqualToBasicRackRootFilletRadius",
        )

        if temp is None:
            return False

        return temp

    @internal_gear_root_fillet_radius_is_always_equal_to_basic_rack_root_fillet_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def internal_gear_root_fillet_radius_is_always_equal_to_basic_rack_root_fillet_radius(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "InternalGearRootFilletRadiusIsAlwaysEqualToBasicRackRootFilletRadius",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def is_scuffing_licensed_for_current_rating_method(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "IsScuffingLicensedForCurrentRatingMethod"
        )

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def limit_dynamic_factor_if_not_in_main_resonance_range_by_default(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "LimitDynamicFactorIfNotInMainResonanceRangeByDefault"
        )

        if temp is None:
            return False

        return temp

    @limit_dynamic_factor_if_not_in_main_resonance_range_by_default.setter
    @exception_bridge
    @enforce_parameter_types
    def limit_dynamic_factor_if_not_in_main_resonance_range_by_default(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "LimitDynamicFactorIfNotInMainResonanceRangeByDefault",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def limit_micro_geometry_factor_for_the_dynamic_load_by_default(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "LimitMicroGeometryFactorForTheDynamicLoadByDefault"
        )

        if temp is None:
            return False

        return temp

    @limit_micro_geometry_factor_for_the_dynamic_load_by_default.setter
    @exception_bridge
    @enforce_parameter_types
    def limit_micro_geometry_factor_for_the_dynamic_load_by_default(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "LimitMicroGeometryFactorForTheDynamicLoadByDefault",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def mean_coefficient_of_friction_flash_temperature_method(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MeanCoefficientOfFrictionFlashTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @mean_coefficient_of_friction_flash_temperature_method.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_coefficient_of_friction_flash_temperature_method(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeanCoefficientOfFrictionFlashTemperatureMethod",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def micropitting_rating_method(self: "Self") -> "_567.MicropittingRatingMethod":
        """mastapy.gears.rating.cylindrical.MicropittingRatingMethod"""
        temp = pythonnet_property_get(self.wrapped, "MicropittingRatingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Cylindrical.MicropittingRatingMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical._567", "MicropittingRatingMethod"
        )(value)

    @micropitting_rating_method.setter
    @exception_bridge
    @enforce_parameter_types
    def micropitting_rating_method(
        self: "Self", value: "_567.MicropittingRatingMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Cylindrical.MicropittingRatingMethod"
        )
        pythonnet_property_set(self.wrapped, "MicropittingRatingMethod", value)

    @property
    @exception_bridge
    def number_of_load_strips_for_basic_ltca(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfLoadStripsForBasicLTCA")

        if temp is None:
            return 0

        return temp

    @number_of_load_strips_for_basic_ltca.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_load_strips_for_basic_ltca(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfLoadStripsForBasicLTCA",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_points_along_profile_for_micropitting_calculation(
        self: "Self",
    ) -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsAlongProfileForMicropittingCalculation"
        )

        if temp is None:
            return 0

        return temp

    @number_of_points_along_profile_for_micropitting_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_along_profile_for_micropitting_calculation(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPointsAlongProfileForMicropittingCalculation",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_points_along_profile_for_scuffing_calculation(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsAlongProfileForScuffingCalculation"
        )

        if temp is None:
            return 0

        return temp

    @number_of_points_along_profile_for_scuffing_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_along_profile_for_scuffing_calculation(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPointsAlongProfileForScuffingCalculation",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_points_along_profile_for_tooth_flank_fracture_calculation(
        self: "Self",
    ) -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsAlongProfileForToothFlankFractureCalculation"
        )

        if temp is None:
            return 0

        return temp

    @number_of_points_along_profile_for_tooth_flank_fracture_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_along_profile_for_tooth_flank_fracture_calculation(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPointsAlongProfileForToothFlankFractureCalculation",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_rotations_for_basic_ltca(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfRotationsForBasicLTCA")

        if temp is None:
            return 0

        return temp

    @number_of_rotations_for_basic_ltca.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_rotations_for_basic_ltca(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfRotationsForBasicLTCA",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def override_default_coefficient_of_friction_calculation_method(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "OverrideDefaultCoefficientOfFrictionCalculationMethod"
        )

        if temp is None:
            return False

        return temp

    @override_default_coefficient_of_friction_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def override_default_coefficient_of_friction_calculation_method(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideDefaultCoefficientOfFrictionCalculationMethod",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def permissible_bending_stress_method(self: "Self") -> "_570.RatingMethod":
        """mastapy.gears.rating.cylindrical.RatingMethod"""
        temp = pythonnet_property_get(self.wrapped, "PermissibleBendingStressMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Cylindrical.RatingMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical._570", "RatingMethod"
        )(value)

    @permissible_bending_stress_method.setter
    @exception_bridge
    @enforce_parameter_types
    def permissible_bending_stress_method(
        self: "Self", value: "_570.RatingMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Cylindrical.RatingMethod"
        )
        pythonnet_property_set(self.wrapped, "PermissibleBendingStressMethod", value)

    @property
    @exception_bridge
    def rating_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_CylindricalGearRatingMethods":
        """EnumWithSelectedValue[mastapy.materials.CylindricalGearRatingMethods]"""
        temp = pythonnet_property_get(self.wrapped, "RatingMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CylindricalGearRatingMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @rating_method.setter
    @exception_bridge
    @enforce_parameter_types
    def rating_method(self: "Self", value: "_338.CylindricalGearRatingMethods") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CylindricalGearRatingMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "RatingMethod", value)

    @property
    @exception_bridge
    def scuffing_rating_method_flash_temperature_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod":
        """EnumWithSelectedValue[mastapy.gears.rating.cylindrical.ScuffingFlashTemperatureRatingMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingRatingMethodFlashTemperatureMethod"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @scuffing_rating_method_flash_temperature_method.setter
    @exception_bridge
    @enforce_parameter_types
    def scuffing_rating_method_flash_temperature_method(
        self: "Self", value: "_572.ScuffingFlashTemperatureRatingMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "ScuffingRatingMethodFlashTemperatureMethod", value
        )

    @property
    @exception_bridge
    def scuffing_rating_method_integral_temperature_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod":
        """EnumWithSelectedValue[mastapy.gears.rating.cylindrical.ScuffingIntegralTemperatureRatingMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingRatingMethodIntegralTemperatureMethod"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @scuffing_rating_method_integral_temperature_method.setter
    @exception_bridge
    @enforce_parameter_types
    def scuffing_rating_method_integral_temperature_method(
        self: "Self", value: "_573.ScuffingIntegralTemperatureRatingMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "ScuffingRatingMethodIntegralTemperatureMethod", value
        )

    @property
    @exception_bridge
    def show_rating_settings_in_report(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowRatingSettingsInReport")

        if temp is None:
            return False

        return temp

    @show_rating_settings_in_report.setter
    @exception_bridge
    @enforce_parameter_types
    def show_rating_settings_in_report(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowRatingSettingsInReport",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_vdi_rating_when_available(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowVDIRatingWhenAvailable")

        if temp is None:
            return False

        return temp

    @show_vdi_rating_when_available.setter
    @exception_bridge
    @enforce_parameter_types
    def show_vdi_rating_when_available(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowVDIRatingWhenAvailable",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def tip_relief_in_scuffing_calculation(
        self: "Self",
    ) -> "_577.TipReliefScuffingOptions":
        """mastapy.gears.rating.cylindrical.TipReliefScuffingOptions"""
        temp = pythonnet_property_get(self.wrapped, "TipReliefInScuffingCalculation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Cylindrical.TipReliefScuffingOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical._577", "TipReliefScuffingOptions"
        )(value)

    @tip_relief_in_scuffing_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def tip_relief_in_scuffing_calculation(
        self: "Self", value: "_577.TipReliefScuffingOptions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Cylindrical.TipReliefScuffingOptions"
        )
        pythonnet_property_set(self.wrapped, "TipReliefInScuffingCalculation", value)

    @property
    @exception_bridge
    def tolerance_rounding_system(self: "Self") -> "_1799.MeasurementSystem":
        """mastapy.utility.units_and_measurements.MeasurementSystem"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceRoundingSystem")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.UnitsAndMeasurements.MeasurementSystem"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.units_and_measurements._1799", "MeasurementSystem"
        )(value)

    @tolerance_rounding_system.setter
    @exception_bridge
    @enforce_parameter_types
    def tolerance_rounding_system(
        self: "Self", value: "_1799.MeasurementSystem"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.UnitsAndMeasurements.MeasurementSystem"
        )
        pythonnet_property_set(self.wrapped, "ToleranceRoundingSystem", value)

    @property
    @exception_bridge
    def use_10_for_contact_ratio_factor_contact_for_spur_gears_with_contact_ratio_less_than_20(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "Use10ForContactRatioFactorContactForSpurGearsWithContactRatioLessThan20",
        )

        if temp is None:
            return False

        return temp

    @use_10_for_contact_ratio_factor_contact_for_spur_gears_with_contact_ratio_less_than_20.setter
    @exception_bridge
    @enforce_parameter_types
    def use_10_for_contact_ratio_factor_contact_for_spur_gears_with_contact_ratio_less_than_20(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "Use10ForContactRatioFactorContactForSpurGearsWithContactRatioLessThan20",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_diametral_pitch(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDiametralPitch")

        if temp is None:
            return False

        return temp

    @use_diametral_pitch.setter
    @exception_bridge
    @enforce_parameter_types
    def use_diametral_pitch(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDiametralPitch",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_interpolated_single_pair_tooth_contact_factor_for_hcr_helical_gears(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "UseInterpolatedSinglePairToothContactFactorForHCRHelicalGears",
        )

        if temp is None:
            return False

        return temp

    @use_interpolated_single_pair_tooth_contact_factor_for_hcr_helical_gears.setter
    @exception_bridge
    @enforce_parameter_types
    def use_interpolated_single_pair_tooth_contact_factor_for_hcr_helical_gears(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseInterpolatedSinglePairToothContactFactorForHCRHelicalGears",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_ltca_stresses_in_gear_rating(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseLTCAStressesInGearRating")

        if temp is None:
            return False

        return temp

    @use_ltca_stresses_in_gear_rating.setter
    @exception_bridge
    @enforce_parameter_types
    def use_ltca_stresses_in_gear_rating(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseLTCAStressesInGearRating",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_point_of_highest_stress_to_calculate_face_load_factor(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UsePointOfHighestStressToCalculateFaceLoadFactor"
        )

        if temp is None:
            return False

        return temp

    @use_point_of_highest_stress_to_calculate_face_load_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def use_point_of_highest_stress_to_calculate_face_load_factor(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UsePointOfHighestStressToCalculateFaceLoadFactor",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def vdi_rating_geometry_calculation_method(
        self: "Self",
    ) -> "overridable.Overridable_CylindricalGearRatingMethods":
        """Overridable[mastapy.materials.CylindricalGearRatingMethods]"""
        temp = pythonnet_property_get(
            self.wrapped, "VDIRatingGeometryCalculationMethod"
        )

        if temp is None:
            return None

        value = overridable.Overridable_CylindricalGearRatingMethods.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @vdi_rating_geometry_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def vdi_rating_geometry_calculation_method(
        self: "Self",
        value: "Union[_338.CylindricalGearRatingMethods, Tuple[_338.CylindricalGearRatingMethods, bool]]",
    ) -> None:
        wrapper_type = (
            overridable.Overridable_CylindricalGearRatingMethods.wrapper_type()
        )
        enclosed_type = (
            overridable.Overridable_CylindricalGearRatingMethods.implicit_type()
        )
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "VDIRatingGeometryCalculationMethod", value
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearDesignAndRatingSettingsItem":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearDesignAndRatingSettingsItem
        """
        return _Cast_CylindricalGearDesignAndRatingSettingsItem(self)
