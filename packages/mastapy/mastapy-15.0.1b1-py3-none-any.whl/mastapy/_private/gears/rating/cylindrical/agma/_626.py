"""AGMA2101MeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.cylindrical import _558

_AGMA2101_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.AGMA", "AGMA2101MeshSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1137, _1185
    from mastapy._private.gears.rating import _457
    from mastapy._private.gears.rating.cylindrical.agma import _625, _628
    from mastapy._private.materials import _344

    Self = TypeVar("Self", bound="AGMA2101MeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMA2101MeshSingleFlankRating._Cast_AGMA2101MeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMA2101MeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMA2101MeshSingleFlankRating:
    """Special nested class for casting AGMA2101MeshSingleFlankRating to subclasses."""

    __parent__: "AGMA2101MeshSingleFlankRating"

    @property
    def cylindrical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_558.CylindricalMeshSingleFlankRating":
        return self.__parent__._cast(_558.CylindricalMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_457.MeshSingleFlankRating":
        from mastapy._private.gears.rating import _457

        return self.__parent__._cast(_457.MeshSingleFlankRating)

    @property
    def agma2101_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "AGMA2101MeshSingleFlankRating":
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
class AGMA2101MeshSingleFlankRating(_558.CylindricalMeshSingleFlankRating):
    """AGMA2101MeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA2101_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_length_of_line_of_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveLengthOfLineOfContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def actual_tangential_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActualTangentialLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def approximate_standard_deviation_of_scuffing_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ApproximateStandardDeviationOfScuffingTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_roughness_ra(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageRoughnessRa")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bearing_span(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingSpan")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def combined_derating_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CombinedDeratingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def composite_surface_roughness_at_fc(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CompositeSurfaceRoughnessAtFC")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_load_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactLoadFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_viscosity_at_reference_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DynamicViscosityAtReferenceTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elastic_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def entraining_velocity_at_end_of_active_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EntrainingVelocityAtEndOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def entraining_velocity_at_pitch_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EntrainingVelocityAtPitchPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def entraining_velocity_at_start_of_active_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EntrainingVelocityAtStartOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_load_distribution_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceLoadDistributionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fifth_distance_along_line_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FifthDistanceAlongLineOfAction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def filter_cutoff_wavelength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FilterCutoffWavelength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def first_distance_along_line_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FirstDistanceAlongLineOfAction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fourth_distance_along_line_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FourthDistanceAlongLineOfAction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gearing_type(self: "Self") -> "_344.GearingTypes":
        """mastapy.materials.GearingTypes

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Materials.GearingTypes")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._344", "GearingTypes"
        )(value)

    @property
    @exception_bridge
    def geometry_factor_i(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorI")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helical_overlap_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelicalOverlapFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def improved_gearing(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ImprovedGearing")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def lead_correction_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadCorrectionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_distribution_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_distribution_factor_source(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactorSource")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def load_sharing_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadSharingRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def materials_parameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialsParameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_contact_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumContactTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumFlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_coefficient_of_friction_calculated_constant_flash_temperature_method(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MeanCoefficientOfFrictionCalculatedConstantFlashTemperatureMethod",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_minimum_specific_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanMinimumSpecificFilmThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_alignment_correction_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshAlignmentCorrectionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_alignment_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshAlignmentFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_alignment_factor_empirical_constant_a(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshAlignmentFactorEmpiricalConstantA"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_alignment_factor_empirical_constant_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshAlignmentFactorEmpiricalConstantB"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_alignment_factor_empirical_constant_c(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshAlignmentFactorEmpiricalConstantC"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_contact_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumContactLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_film_thickness_isothermal(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumFilmThicknessIsothermal")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_film_thickness_with_inlet_shear_heating(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumFilmThicknessWithInletShearHeating"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_length_of_contact_lines_per_unit_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLengthOfContactLinesPerUnitModule"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_specific_film_thickness_isothermal(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumSpecificFilmThicknessIsothermal"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_specific_film_thickness_with_inlet_shear_heating(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumSpecificFilmThicknessWithInletShearHeating"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_operating_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalOperatingLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_unit_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalUnitLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def operating_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def overload_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverloadFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def parameter_for_calculating_tooth_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParameterForCalculatingToothTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_offset_from_bearing(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionOffsetFromBearing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_proportion_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionProportionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_proportion_modifier(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionProportionModifier")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pressure_viscosity_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureViscosityCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def probability_of_scuffing(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProbabilityOfScuffing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def probability_of_wear_isothermal(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProbabilityOfWearIsothermal")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def probability_of_wear_with_inlet_shear_heating(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProbabilityOfWearWithInletShearHeating"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def profile_modification(
        self: "Self",
    ) -> "_1137.CylindricalGearProfileModifications":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileModifications

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileModification")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CylindricalGearProfileModifications",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1137",
            "CylindricalGearProfileModifications",
        )(value)

    @property
    @exception_bridge
    def rating_standard_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingStandardName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def reference_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_temperature_method(
        self: "Self",
    ) -> "_1185.ScuffingTemperatureMethodsAGMA":
        """mastapy.gears.gear_designs.cylindrical.ScuffingTemperatureMethodsAGMA

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingTemperatureMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ScuffingTemperatureMethodsAGMA",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1185",
            "ScuffingTemperatureMethodsAGMA",
        )(value)

    @property
    @exception_bridge
    def second_distance_along_line_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SecondDistanceAlongLineOfAction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sixth_distance_along_line_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SixthDistanceAlongLineOfAction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def size_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_velocity_at_end_of_active_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingVelocityAtEndOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_velocity_at_pitch_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingVelocityAtPitchPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_velocity_at_start_of_active_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingVelocityAtStartOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def standard_deviation_of_the_minimum_specific_film_thickness(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StandardDeviationOfTheMinimumSpecificFilmThickness"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sump_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SumpTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_condition_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceConditionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_roughness_constant(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceRoughnessConstant")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def temperature_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TemperatureFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def temperature_viscosity_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TemperatureViscosityCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def third_distance_along_line_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThirdDistanceAlongLineOfAction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transmission_accuracy_number(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmissionAccuracyNumber")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_load_distribution_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseLoadDistributionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_metric_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseMetricModule")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def thermal_reduction_factor_factors_and_exponents(
        self: "Self",
    ) -> "_628.ThermalReductionFactorFactorsAndExponents":
        """mastapy.gears.rating.cylindrical.agma.ThermalReductionFactorFactorsAndExponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThermalReductionFactorFactorsAndExponents"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_625.AGMA2101GearSingleFlankRating]":
        """List[mastapy.gears.rating.cylindrical.agma.AGMA2101GearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSingleFlankRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def agma_cylindrical_gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_625.AGMA2101GearSingleFlankRating]":
        """List[mastapy.gears.rating.cylindrical.agma.AGMA2101GearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMACylindricalGearSingleFlankRatings"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AGMA2101MeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_AGMA2101MeshSingleFlankRating
        """
        return _Cast_AGMA2101MeshSingleFlankRating(self)
