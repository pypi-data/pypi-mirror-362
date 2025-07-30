"""AGMAScuffingResultsRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.rating.cylindrical import _575

_AGMA_SCUFFING_RESULTS_ROW = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "AGMAScuffingResultsRow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AGMAScuffingResultsRow")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMAScuffingResultsRow._Cast_AGMAScuffingResultsRow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAScuffingResultsRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAScuffingResultsRow:
    """Special nested class for casting AGMAScuffingResultsRow to subclasses."""

    __parent__: "AGMAScuffingResultsRow"

    @property
    def scuffing_results_row(self: "CastSelf") -> "_575.ScuffingResultsRow":
        return self.__parent__._cast(_575.ScuffingResultsRow)

    @property
    def agma_scuffing_results_row(self: "CastSelf") -> "AGMAScuffingResultsRow":
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
class AGMAScuffingResultsRow(_575.ScuffingResultsRow):
    """AGMAScuffingResultsRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_SCUFFING_RESULTS_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def central_film_thickness_isothermal(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CentralFilmThicknessIsothermal")

        if temp is None:
            return 0.0

        return temp

    @central_film_thickness_isothermal.setter
    @exception_bridge
    @enforce_parameter_types
    def central_film_thickness_isothermal(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CentralFilmThicknessIsothermal",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def central_film_thickness_with_inlet_shear_heating(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "CentralFilmThicknessWithInletShearHeating"
        )

        if temp is None:
            return 0.0

        return temp

    @central_film_thickness_with_inlet_shear_heating.setter
    @exception_bridge
    @enforce_parameter_types
    def central_film_thickness_with_inlet_shear_heating(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CentralFilmThicknessWithInletShearHeating",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def contact_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ContactTemperature")

        if temp is None:
            return 0.0

        return temp

    @contact_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ContactTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def dimensionless_central_film_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DimensionlessCentralFilmThickness")

        if temp is None:
            return 0.0

        return temp

    @dimensionless_central_film_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def dimensionless_central_film_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DimensionlessCentralFilmThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def flash_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @flash_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def flash_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FlashTemperature", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def hertzian_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HertzianStress")

        if temp is None:
            return 0.0

        return temp

    @hertzian_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def hertzian_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HertzianStress", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def load_parameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LoadParameter")

        if temp is None:
            return 0.0

        return temp

    @load_parameter.setter
    @exception_bridge
    @enforce_parameter_types
    def load_parameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LoadParameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def mean_coefficient_of_friction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanCoefficientOfFriction")

        if temp is None:
            return 0.0

        return temp

    @mean_coefficient_of_friction.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_coefficient_of_friction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeanCoefficientOfFriction",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pinion_rolling_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinionRollingVelocity")

        if temp is None:
            return 0.0

        return temp

    @pinion_rolling_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def pinion_rolling_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinionRollingVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def semi_width_of_hertzian_contact_band(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SemiWidthOfHertzianContactBand")

        if temp is None:
            return 0.0

        return temp

    @semi_width_of_hertzian_contact_band.setter
    @exception_bridge
    @enforce_parameter_types
    def semi_width_of_hertzian_contact_band(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SemiWidthOfHertzianContactBand",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def slideto_roll_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SlidetoRollRatio")

        if temp is None:
            return 0.0

        return temp

    @slideto_roll_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def slideto_roll_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SlidetoRollRatio", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def sliding_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SlidingVelocity")

        if temp is None:
            return 0.0

        return temp

    @sliding_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def sliding_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SlidingVelocity", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def specific_film_thickness_with_filter_cutoff_wavelength_isothermal(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "SpecificFilmThicknessWithFilterCutoffWavelengthIsothermal"
        )

        if temp is None:
            return 0.0

        return temp

    @specific_film_thickness_with_filter_cutoff_wavelength_isothermal.setter
    @exception_bridge
    @enforce_parameter_types
    def specific_film_thickness_with_filter_cutoff_wavelength_isothermal(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecificFilmThicknessWithFilterCutoffWavelengthIsothermal",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def specific_film_thickness_with_filter_cutoff_wavelength_with_inlet_shear_heating(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped,
            "SpecificFilmThicknessWithFilterCutoffWavelengthWithInletShearHeating",
        )

        if temp is None:
            return 0.0

        return temp

    @specific_film_thickness_with_filter_cutoff_wavelength_with_inlet_shear_heating.setter
    @exception_bridge
    @enforce_parameter_types
    def specific_film_thickness_with_filter_cutoff_wavelength_with_inlet_shear_heating(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecificFilmThicknessWithFilterCutoffWavelengthWithInletShearHeating",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def speed_parameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpeedParameter")

        if temp is None:
            return 0.0

        return temp

    @speed_parameter.setter
    @exception_bridge
    @enforce_parameter_types
    def speed_parameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SpeedParameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def thermal_loading_parameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ThermalLoadingParameter")

        if temp is None:
            return 0.0

        return temp

    @thermal_loading_parameter.setter
    @exception_bridge
    @enforce_parameter_types
    def thermal_loading_parameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ThermalLoadingParameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def thermal_reduction_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ThermalReductionFactor")

        if temp is None:
            return 0.0

        return temp

    @thermal_reduction_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def thermal_reduction_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ThermalReductionFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def wheel_rolling_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelRollingVelocity")

        if temp is None:
            return 0.0

        return temp

    @wheel_rolling_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_rolling_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelRollingVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAScuffingResultsRow":
        """Cast to another type.

        Returns:
            _Cast_AGMAScuffingResultsRow
        """
        return _Cast_AGMAScuffingResultsRow(self)
