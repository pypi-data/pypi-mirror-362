"""LoadedTiltingPadJournalBearingResults"""

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
from mastapy._private.bearings.bearing_results.fluid_film import _2331

_LOADED_TILTING_PAD_JOURNAL_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.FluidFilm",
    "LoadedTiltingPadJournalBearingResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2078
    from mastapy._private.bearings.bearing_results import _2155, _2160, _2163
    from mastapy._private.bearings.bearing_results.fluid_film import _2329

    Self = TypeVar("Self", bound="LoadedTiltingPadJournalBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedTiltingPadJournalBearingResults._Cast_LoadedTiltingPadJournalBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedTiltingPadJournalBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedTiltingPadJournalBearingResults:
    """Special nested class for casting LoadedTiltingPadJournalBearingResults to subclasses."""

    __parent__: "LoadedTiltingPadJournalBearingResults"

    @property
    def loaded_pad_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2331.LoadedPadFluidFilmBearingResults":
        return self.__parent__._cast(_2331.LoadedPadFluidFilmBearingResults)

    @property
    def loaded_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2329.LoadedFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2329

        return self.__parent__._cast(_2329.LoadedFluidFilmBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2160.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2160

        return self.__parent__._cast(_2160.LoadedDetailedBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2163.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2163

        return self.__parent__._cast(_2163.LoadedNonLinearBearingResults)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2155.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2155

        return self.__parent__._cast(_2155.LoadedBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_2078.BearingLoadCaseResultsLightweight":
        from mastapy._private.bearings import _2078

        return self.__parent__._cast(_2078.BearingLoadCaseResultsLightweight)

    @property
    def loaded_tilting_pad_journal_bearing_results(
        self: "CastSelf",
    ) -> "LoadedTiltingPadJournalBearingResults":
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
class LoadedTiltingPadJournalBearingResults(_2331.LoadedPadFluidFilmBearingResults):
    """LoadedTiltingPadJournalBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_TILTING_PAD_JOURNAL_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_position_of_the_minimum_film_thickness_from_the_x_axis(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngularPositionOfTheMinimumFilmThicknessFromTheXAxis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def critical_reynolds_number(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CriticalReynoldsNumber")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def eccentricity_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EccentricityRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def effective_film_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EffectiveFilmTemperature")

        if temp is None:
            return 0.0

        return temp

    @effective_film_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def effective_film_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EffectiveFilmTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def exit_flow(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExitFlow")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force_in_direction_of_eccentricity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceInDirectionOfEccentricity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_preload_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HydrodynamicPreloadFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inlet_flow(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InletFlow")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_density(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantDensity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_dynamic_viscosity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantDynamicViscosity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_pad_eccentricity_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPadEccentricityRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_pressure_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPressureVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumFilmThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def non_dimensional_friction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalFriction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def non_dimensional_maximum_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalMaximumPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def non_dimensional_minimum_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NonDimensionalMinimumFilmThickness"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def non_dimensional_out_flow(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalOutFlow")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def non_dimensional_side_flow(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalSideFlow")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pad_shape_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PadShapeFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reynolds_number(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReynoldsNumber")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def side_flow(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SideFlow")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sommerfeld_number(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SommerfeldNumber")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedTiltingPadJournalBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedTiltingPadJournalBearingResults
        """
        return _Cast_LoadedTiltingPadJournalBearingResults(self)
