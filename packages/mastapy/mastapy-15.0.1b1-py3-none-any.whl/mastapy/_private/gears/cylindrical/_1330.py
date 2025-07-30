"""CylindricalGearWorstLTCAContactChartDataAsTextFile"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)

_CYLINDRICAL_GEAR_WORST_LTCA_CONTACT_CHART_DATA_AS_TEXT_FILE = python_net_import(
    "SMT.MastaAPI.Gears.Cylindrical",
    "CylindricalGearWorstLTCAContactChartDataAsTextFile",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearWorstLTCAContactChartDataAsTextFile")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearWorstLTCAContactChartDataAsTextFile._Cast_CylindricalGearWorstLTCAContactChartDataAsTextFile",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearWorstLTCAContactChartDataAsTextFile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearWorstLTCAContactChartDataAsTextFile:
    """Special nested class for casting CylindricalGearWorstLTCAContactChartDataAsTextFile to subclasses."""

    __parent__: "CylindricalGearWorstLTCAContactChartDataAsTextFile"

    @property
    def cylindrical_gear_worst_ltca_contact_chart_data_as_text_file(
        self: "CastSelf",
    ) -> "CylindricalGearWorstLTCAContactChartDataAsTextFile":
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
class CylindricalGearWorstLTCAContactChartDataAsTextFile(_0.APIBase):
    """CylindricalGearWorstLTCAContactChartDataAsTextFile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYLINDRICAL_GEAR_WORST_LTCA_CONTACT_CHART_DATA_AS_TEXT_FILE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    def coefficient_of_friction(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CoefficientOfFriction")

    @exception_bridge
    def depth_of_max_shear_stress(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DepthOfMaxShearStress")

    @exception_bridge
    def force_per_unit_length(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ForcePerUnitLength")

    @exception_bridge
    def gap_between_loaded_flanks_transverse(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GapBetweenLoadedFlanksTransverse")

    @exception_bridge
    def gap_between_unloaded_flanks_transverse(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GapBetweenUnloadedFlanksTransverse")

    @exception_bridge
    def gear_a_depth_of_maximum_material_exposure_iso633642019(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "GearADepthOfMaximumMaterialExposureISO633642019"
        )

    @exception_bridge
    def gear_a_maximum_material_exposure_iso633642019(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GearAMaximumMaterialExposureISO633642019")

    @exception_bridge
    def gear_b_depth_of_maximum_material_exposure_iso633642019(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "GearBDepthOfMaximumMaterialExposureISO633642019"
        )

    @exception_bridge
    def gear_b_maximum_material_exposure_iso633642019(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GearBMaximumMaterialExposureISO633642019")

    @exception_bridge
    def hertzian_contact_half_width(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "HertzianContactHalfWidth")

    @exception_bridge
    def lubrication_state_d_value(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "LubricationStateDValue")

    @exception_bridge
    def max_pressure(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "MaxPressure")

    @exception_bridge
    def max_shear_stress(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "MaxShearStress")

    @exception_bridge
    def micropitting_contact_temperature_isotr1514412010(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "MicropittingContactTemperatureISOTR1514412010"
        )

    @exception_bridge
    def micropitting_contact_temperature_isotr1514412014(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "MicropittingContactTemperatureISOTR1514412014"
        )

    @exception_bridge
    def micropitting_contact_temperature_isots6336222018(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "MicropittingContactTemperatureISOTS6336222018"
        )

    @exception_bridge
    def micropitting_flash_temperature_isotr1514412010(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "MicropittingFlashTemperatureISOTR1514412010"
        )

    @exception_bridge
    def micropitting_flash_temperature_isotr1514412014(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "MicropittingFlashTemperatureISOTR1514412014"
        )

    @exception_bridge
    def micropitting_flash_temperature_isots6336222018(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "MicropittingFlashTemperatureISOTS6336222018"
        )

    @exception_bridge
    def micropitting_safety_factor_isotr1514412010(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "MicropittingSafetyFactorISOTR1514412010")

    @exception_bridge
    def micropitting_safety_factor_isotr1514412014(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "MicropittingSafetyFactorISOTR1514412014")

    @exception_bridge
    def micropitting_safety_factor_isots6336222018(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "MicropittingSafetyFactorISOTS6336222018")

    @exception_bridge
    def minimum_lubricant_film_thickness_dowson(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "MinimumLubricantFilmThicknessDowson")

    @exception_bridge
    def minimum_lubricant_film_thickness_isotr1514412010(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "MinimumLubricantFilmThicknessISOTR1514412010"
        )

    @exception_bridge
    def minimum_lubricant_film_thickness_isotr1514412014(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "MinimumLubricantFilmThicknessISOTR1514412014"
        )

    @exception_bridge
    def minimum_lubricant_film_thickness_isots6336222018(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "MinimumLubricantFilmThicknessISOTS6336222018"
        )

    @exception_bridge
    def pressure_velocity_pv(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PressureVelocityPV")

    @exception_bridge
    def scuffing_contact_temperature_agma925a03(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingContactTemperatureAGMA925A03")

    @exception_bridge
    def scuffing_contact_temperature_agma925b22(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingContactTemperatureAGMA925B22")

    @exception_bridge
    def scuffing_contact_temperature_din399041987(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingContactTemperatureDIN399041987")

    @exception_bridge
    def scuffing_contact_temperature_isotr1398912000(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingContactTemperatureISOTR1398912000")

    @exception_bridge
    def scuffing_contact_temperature_isots6336202017(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingContactTemperatureISOTS6336202017")

    @exception_bridge
    def scuffing_contact_temperature_isots6336202022(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingContactTemperatureISOTS6336202022")

    @exception_bridge
    def scuffing_flash_temperature_agma925a03(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingFlashTemperatureAGMA925A03")

    @exception_bridge
    def scuffing_flash_temperature_agma925b22(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingFlashTemperatureAGMA925B22")

    @exception_bridge
    def scuffing_flash_temperature_din399041987(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingFlashTemperatureDIN399041987")

    @exception_bridge
    def scuffing_flash_temperature_isotr1398912000(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingFlashTemperatureISOTR1398912000")

    @exception_bridge
    def scuffing_flash_temperature_isots6336202017(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingFlashTemperatureISOTS6336202017")

    @exception_bridge
    def scuffing_flash_temperature_isots6336202022(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingFlashTemperatureISOTS6336202022")

    @exception_bridge
    def scuffing_safety_factor_agma925a03(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingSafetyFactorAGMA925A03")

    @exception_bridge
    def scuffing_safety_factor_agma925b22(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingSafetyFactorAGMA925B22")

    @exception_bridge
    def scuffing_safety_factor_din399041987(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingSafetyFactorDIN399041987")

    @exception_bridge
    def scuffing_safety_factor_isotr1398912000(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingSafetyFactorISOTR1398912000")

    @exception_bridge
    def scuffing_safety_factor_isots6336202017(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingSafetyFactorISOTS6336202017")

    @exception_bridge
    def scuffing_safety_factor_isots6336202022(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ScuffingSafetyFactorISOTS6336202022")

    @exception_bridge
    def sliding_power_loss(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SlidingPowerLoss")

    @exception_bridge
    def sliding_velocity(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SlidingVelocity")

    @exception_bridge
    def specific_lubricant_film_thickness_isotr1514412010(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "SpecificLubricantFilmThicknessISOTR1514412010"
        )

    @exception_bridge
    def specific_lubricant_film_thickness_isotr1514412014(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "SpecificLubricantFilmThicknessISOTR1514412014"
        )

    @exception_bridge
    def specific_lubricant_film_thickness_isots6336222018(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "SpecificLubricantFilmThicknessISOTS6336222018"
        )

    @exception_bridge
    def total_deflection_for_mesh(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "TotalDeflectionForMesh")

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CylindricalGearWorstLTCAContactChartDataAsTextFile":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearWorstLTCAContactChartDataAsTextFile
        """
        return _Cast_CylindricalGearWorstLTCAContactChartDataAsTextFile(self)
