"""ISO6336AbstractMetalMeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.cylindrical.iso6336 import _609

_ISO6336_ABSTRACT_METAL_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "ISO6336AbstractMetalMeshSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1186
    from mastapy._private.gears.rating import _457
    from mastapy._private.gears.rating.cylindrical import _550, _558, _567, _572, _573
    from mastapy._private.gears.rating.cylindrical.din3990 import _624
    from mastapy._private.gears.rating.cylindrical.iso6336 import _603, _605, _607, _610

    Self = TypeVar("Self", bound="ISO6336AbstractMetalMeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO6336AbstractMetalMeshSingleFlankRating._Cast_ISO6336AbstractMetalMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO6336AbstractMetalMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO6336AbstractMetalMeshSingleFlankRating:
    """Special nested class for casting ISO6336AbstractMetalMeshSingleFlankRating to subclasses."""

    __parent__: "ISO6336AbstractMetalMeshSingleFlankRating"

    @property
    def iso6336_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_609.ISO6336AbstractMeshSingleFlankRating":
        return self.__parent__._cast(_609.ISO6336AbstractMeshSingleFlankRating)

    @property
    def cylindrical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_558.CylindricalMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _558

        return self.__parent__._cast(_558.CylindricalMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_457.MeshSingleFlankRating":
        from mastapy._private.gears.rating import _457

        return self.__parent__._cast(_457.MeshSingleFlankRating)

    @property
    def iso63361996_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_603.ISO63361996MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _603

        return self.__parent__._cast(_603.ISO63361996MeshSingleFlankRating)

    @property
    def iso63362006_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_605.ISO63362006MeshSingleFlankRating":
        return self.__parent__._cast(_605.ISO63362006MeshSingleFlankRating)

    @property
    def iso63362019_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_607.ISO63362019MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _607

        return self.__parent__._cast(_607.ISO63362019MeshSingleFlankRating)

    @property
    def din3990_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_624.DIN3990MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.din3990 import _624

        return self.__parent__._cast(_624.DIN3990MeshSingleFlankRating)

    @property
    def iso6336_abstract_metal_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "ISO6336AbstractMetalMeshSingleFlankRating":
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
class ISO6336AbstractMetalMeshSingleFlankRating(
    _609.ISO6336AbstractMeshSingleFlankRating
):
    """ISO6336AbstractMetalMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO6336_ABSTRACT_METAL_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_stress_number_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableStressNumberContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def angle_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngleFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def approach_factor_integral(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ApproachFactorIntegral")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def approach_factor_of_maximum_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ApproachFactorOfMaximumFlashTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageFlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_mean_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicMeanFlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_rack_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRackFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bulk_temperature_for_micropitting(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BulkTemperatureForMicropitting")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bulk_tooth_temperature_flash_temperature_method(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BulkToothTemperatureFlashTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bulk_tooth_temperature_integral_temperature_method(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BulkToothTemperatureIntegralTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_exposure_time_flash_temperature_method(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactExposureTimeFlashTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_exposure_time_integral_temperature_method(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactExposureTimeIntegralTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_ratio_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactRatioFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_time_at_high_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactTimeAtHighVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_time_at_medium_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactTimeAtMediumVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def determinant_tangential_load_in_transverse_plane_for_transverse_load_factor(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DeterminantTangentialLoadInTransversePlaneForTransverseLoadFactor",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def drive_gear_tip_relief(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DriveGearTipRelief")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_factor_source(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicFactorSource")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def effective_equivalent_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveEquivalentMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def effective_profile_form_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveProfileFormDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def effective_tip_relief(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveTipRelief")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def effective_transverse_base_pitch_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EffectiveTransverseBasePitchDeviation"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def equivalent_misalignment_due_to_system_deflection(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EquivalentMisalignmentDueToSystemDeflection"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def equivalent_tip_relief_of_pinion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EquivalentTipReliefOfPinion")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def equivalent_tip_relief_of_wheel(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EquivalentTipReliefOfWheel")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_load_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceLoadFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_load_factor_contact_source(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceLoadFactorContactSource")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def gear_blank_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBlankFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def geometry_factor_at_pinion_tooth_tip(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorAtPinionToothTip")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helical_load_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelicalLoadFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def highest_local_contact_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HighestLocalContactTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def initial_equivalent_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InitialEquivalentMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def integral_contact_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IntegralContactTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def integral_scuffing_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IntegralScuffingTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_path_of_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthOfPathOfContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def limiting_specific_lubricant_film_thickness_of_the_test_gears(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LimitingSpecificLubricantFilmThicknessOfTheTestGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_losses_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadLossesFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def local_hertzian_contact_stress_calculation_method(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LocalHertzianContactStressCalculationMethod"
        )

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def longest_contact_exposure_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LongestContactExposureTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def longest_contact_exposure_time_integral(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LongestContactExposureTimeIntegral"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_density_at_156_degrees_celsius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LubricantDensityAt156DegreesCelsius"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_density_at_bulk_tooth_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LubricantDensityAtBulkToothTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_density_at_micropitting_bulk_tooth_temperature(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LubricantDensityAtMicropittingBulkToothTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_dynamic_viscosity_at_tooth_temperature_micropitting(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LubricantDynamicViscosityAtToothTemperatureMicropitting"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_factor_flash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantFactorFlash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_factor_integral(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantFactorIntegral")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubrication_system_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricationSystemFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def material_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def material_parameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialParameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_base_pitch_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumBasePitchDeviation")

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
    def maximum_profile_form_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumProfileFormDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_coefficient_of_friction_integral_temperature_method(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanCoefficientOfFrictionIntegralTemperatureMethod"
        )

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
    def mean_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanFlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_misalignment_due_to_manufacturing_deviations(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshMisalignmentDueToManufacturingDeviations"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def mesh_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def micro_geometry_factor_for_the_dynamic_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicroGeometryFactorForTheDynamicLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def micropitting_rating_method(self: "Self") -> "_567.MicropittingRatingMethod":
        """mastapy.gears.rating.cylindrical.MicropittingRatingMethod

        Note:
            This property is readonly.
        """
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

    @property
    @exception_bridge
    def micropitting_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicropittingSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lubricant_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumLubricantFilmThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_specific_lubricant_film_thickness_in_the_contact_area(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumSpecificLubricantFilmThicknessInTheContactArea"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def misalignment_due_to_micro_geometry_lead_relief(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MisalignmentDueToMicroGeometryLeadRelief"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def multiple_path_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MultiplePathFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_relative_radius_of_curvature_at_pitch_point_integral_temperature_method(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "NormalRelativeRadiusOfCurvatureAtPitchPointIntegralTemperatureMethod",
        )

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
    def optimal_tip_relief(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OptimalTipRelief")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_specific_lubricant_film_thickness(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleSpecificLubricantFilmThickness"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def permissible_specific_lubricant_film_thickness_from_figure_a1(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleSpecificLubricantFilmThicknessFromFigureA1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pressure_viscosity_coefficient_at_38_degrees_c(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PressureViscosityCoefficientAt38DegreesC"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pressure_viscosity_coefficient_at_bulk_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PressureViscosityCoefficientAtBulkTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def profile_form_deviation_factor_for_the_dynamic_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileFormDeviationFactorForTheDynamicLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_mass_per_unit_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeMassPerUnitFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_welding_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeWeldingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def resonance_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResonanceRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def resonance_ratio_in_the_main_resonance_range(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ResonanceRatioInTheMainResonanceRange"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def resonance_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResonanceSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def roughness_factor_micropitting(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughnessFactorMicropitting")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def run_in_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RunInFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def run_in_grade(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RunInGrade")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def running_in(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RunningIn")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def running_in_profile_form_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RunningInProfileFormDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def running_in_allowance_equivalent_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RunningInAllowanceEquivalentMisalignment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_load_safety_factor_integral_temperature_method(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingLoadSafetyFactorIntegralTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_rating_method_flash_temperature_method(
        self: "Self",
    ) -> "_572.ScuffingFlashTemperatureRatingMethod":
        """mastapy.gears.rating.cylindrical.ScuffingFlashTemperatureRatingMethod

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingRatingMethodFlashTemperatureMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Rating.Cylindrical.ScuffingFlashTemperatureRatingMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical._572",
            "ScuffingFlashTemperatureRatingMethod",
        )(value)

    @property
    @exception_bridge
    def scuffing_rating_method_integral_temperature_method(
        self: "Self",
    ) -> "_573.ScuffingIntegralTemperatureRatingMethod":
        """mastapy.gears.rating.cylindrical.ScuffingIntegralTemperatureRatingMethod

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingRatingMethodIntegralTemperatureMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Rating.Cylindrical.ScuffingIntegralTemperatureRatingMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical._573",
            "ScuffingIntegralTemperatureRatingMethod",
        )(value)

    @property
    @exception_bridge
    def scuffing_safety_factor_flash_temperature_method(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingSafetyFactorFlashTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_safety_factor_integral_temperature_method(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingSafetyFactorIntegralTemperatureMethod"
        )

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
    def scuffing_temperature_at_high_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingTemperatureAtHighVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_temperature_at_medium_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingTemperatureAtMediumVelocity"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_temperature_gradient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingTemperatureGradient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_temperature_gradient_integral(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingTemperatureGradientIntegral"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_temperature_method(
        self: "Self",
    ) -> "_1186.ScuffingTemperatureMethodsISO":
        """mastapy.gears.gear_designs.cylindrical.ScuffingTemperatureMethodsISO

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingTemperatureMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ScuffingTemperatureMethodsISO",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1186",
            "ScuffingTemperatureMethodsISO",
        )(value)

    @property
    @exception_bridge
    def single_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SingleStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_material_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessMaterialFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def test_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TestTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def theoretical_single_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TheoreticalSingleStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def thermo_elastic_factor_of_maximum_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThermoElasticFactorOfMaximumFlashTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_relief(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipRelief")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_relief_calculated(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipReliefCalculated")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_relief_factor_integral(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipReliefFactorIntegral")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_relief_factor_for_micropitting(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipReliefFactorForMicropitting")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_stiffness_correction_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothStiffnessCorrectionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_base_pitch_deviation_factor_for_the_dynamic_load(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseBasePitchDeviationFactorForTheDynamicLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_load_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseLoadFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_unit_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseUnitLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def user_input_scuffing_integral_temperature_for_long_contact_times(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UserInputScuffingIntegralTemperatureForLongContactTimes"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def user_input_scuffing_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserInputScuffingTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def user_input_scuffing_temperature_for_long_contact_times(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UserInputScuffingTemperatureForLongContactTimes"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def single_flank_rating_of_test_gears_for_micropitting(
        self: "Self",
    ) -> "_605.ISO63362006MeshSingleFlankRating":
        """mastapy.gears.rating.cylindrical.iso6336.ISO63362006MeshSingleFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SingleFlankRatingOfTestGearsForMicropitting"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sorted_micro_pitting_results(
        self: "Self",
    ) -> "_550.CylindricalGearMicroPittingResults":
        """mastapy.gears.rating.cylindrical.CylindricalGearMicroPittingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SortedMicroPittingResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def isodin_cylindrical_gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_610.ISO6336AbstractMetalGearSingleFlankRating]":
        """List[mastapy.gears.rating.cylindrical.iso6336.ISO6336AbstractMetalGearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISODINCylindricalGearSingleFlankRatings"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ISO6336AbstractMetalMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO6336AbstractMetalMeshSingleFlankRating
        """
        return _Cast_ISO6336AbstractMetalMeshSingleFlankRating(self)
