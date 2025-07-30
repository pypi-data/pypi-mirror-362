"""CylindricalPlanetaryGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical import _1138

_CYLINDRICAL_PLANETARY_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalPlanetaryGearSetDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1052, _1054
    from mastapy._private.math_utility import _1697
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="CylindricalPlanetaryGearSetDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalPlanetaryGearSetDesign._Cast_CylindricalPlanetaryGearSetDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetaryGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalPlanetaryGearSetDesign:
    """Special nested class for casting CylindricalPlanetaryGearSetDesign to subclasses."""

    __parent__: "CylindricalPlanetaryGearSetDesign"

    @property
    def cylindrical_gear_set_design(
        self: "CastSelf",
    ) -> "_1138.CylindricalGearSetDesign":
        return self.__parent__._cast(_1138.CylindricalGearSetDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "_1054.GearSetDesign":
        from mastapy._private.gears.gear_designs import _1054

        return self.__parent__._cast(_1054.GearSetDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def cylindrical_planetary_gear_set_design(
        self: "CastSelf",
    ) -> "CylindricalPlanetaryGearSetDesign":
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
class CylindricalPlanetaryGearSetDesign(_1138.CylindricalGearSetDesign):
    """CylindricalPlanetaryGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_PLANETARY_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def equally_spaced_planets_are_assemblable(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EquallySpacedPlanetsAreAssemblable"
        )

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def in_phase(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InPhase")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def least_mesh_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeastMeshAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_module_scale_planet_diameters(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalModuleScalePlanetDiameters")

        if temp is None:
            return 0.0

        return temp

    @normal_module_scale_planet_diameters.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_module_scale_planet_diameters(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalModuleScalePlanetDiameters",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def planet_gear_phasing_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetGearPhasingChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def reference_fixed_gear_for_planetary_sideband_fourier_series_is_annulus(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ReferenceFixedGearForPlanetarySidebandFourierSeriesIsAnnulus"
        )

        if temp is None:
            return False

        return temp

    @reference_fixed_gear_for_planetary_sideband_fourier_series_is_annulus.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_fixed_gear_for_planetary_sideband_fourier_series_is_annulus(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReferenceFixedGearForPlanetarySidebandFourierSeriesIsAnnulus",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_planet_passing_window_function_in_planetary_sideband_fourier_series(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "UsePlanetPassingWindowFunctionInPlanetarySidebandFourierSeries",
        )

        if temp is None:
            return False

        return temp

    @use_planet_passing_window_function_in_planetary_sideband_fourier_series.setter
    @exception_bridge
    @enforce_parameter_types
    def use_planet_passing_window_function_in_planetary_sideband_fourier_series(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UsePlanetPassingWindowFunctionInPlanetarySidebandFourierSeries",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def planetary_sideband_fourier_series_for_rotating_planet_carrier(
        self: "Self",
    ) -> "_1697.FourierSeries":
        """mastapy.math_utility.FourierSeries

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PlanetarySidebandFourierSeriesForRotatingPlanetCarrier"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def add_new_micro_geometry_using_planetary_duplicates(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "AddNewMicroGeometryUsingPlanetaryDuplicates"
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalPlanetaryGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_CylindricalPlanetaryGearSetDesign
        """
        return _Cast_CylindricalPlanetaryGearSetDesign(self)
