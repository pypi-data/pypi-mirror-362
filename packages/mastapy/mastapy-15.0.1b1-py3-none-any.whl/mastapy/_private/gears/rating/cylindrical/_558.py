"""CylindricalMeshSingleFlankRating"""

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
from mastapy._private.gears.rating import _457

_CYLINDRICAL_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalMeshSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _410
    from mastapy._private.gears.gear_designs.cylindrical import _1183, _1184
    from mastapy._private.gears.rating.cylindrical import _545, _553, _556
    from mastapy._private.gears.rating.cylindrical.agma import _626
    from mastapy._private.gears.rating.cylindrical.din3990 import _624
    from mastapy._private.gears.rating.cylindrical.iso6336 import (
        _603,
        _605,
        _607,
        _609,
        _611,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _581,
        _583,
        _585,
    )
    from mastapy._private.materials import _356

    Self = TypeVar("Self", bound="CylindricalMeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalMeshSingleFlankRating._Cast_CylindricalMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalMeshSingleFlankRating:
    """Special nested class for casting CylindricalMeshSingleFlankRating to subclasses."""

    __parent__: "CylindricalMeshSingleFlankRating"

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_457.MeshSingleFlankRating":
        return self.__parent__._cast(_457.MeshSingleFlankRating)

    @property
    def metal_plastic_or_plastic_metal_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_581.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _581

        return self.__parent__._cast(
            _581.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating
        )

    @property
    def plastic_gear_vdi2736_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_583.PlasticGearVDI2736AbstractMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _583

        return self.__parent__._cast(
            _583.PlasticGearVDI2736AbstractMeshSingleFlankRating
        )

    @property
    def plastic_plastic_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_585.PlasticPlasticVDI2736MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _585

        return self.__parent__._cast(_585.PlasticPlasticVDI2736MeshSingleFlankRating)

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
        from mastapy._private.gears.rating.cylindrical.iso6336 import _605

        return self.__parent__._cast(_605.ISO63362006MeshSingleFlankRating)

    @property
    def iso63362019_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_607.ISO63362019MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _607

        return self.__parent__._cast(_607.ISO63362019MeshSingleFlankRating)

    @property
    def iso6336_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_609.ISO6336AbstractMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _609

        return self.__parent__._cast(_609.ISO6336AbstractMeshSingleFlankRating)

    @property
    def iso6336_abstract_metal_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_611.ISO6336AbstractMetalMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _611

        return self.__parent__._cast(_611.ISO6336AbstractMetalMeshSingleFlankRating)

    @property
    def din3990_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_624.DIN3990MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.din3990 import _624

        return self.__parent__._cast(_624.DIN3990MeshSingleFlankRating)

    @property
    def agma2101_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_626.AGMA2101MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.agma import _626

        return self.__parent__._cast(_626.AGMA2101MeshSingleFlankRating)

    @property
    def cylindrical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "CylindricalMeshSingleFlankRating":
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
class CylindricalMeshSingleFlankRating(_457.MeshSingleFlankRating):
    """CylindricalMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_length_of_the_line_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveLengthOfTheLineOfAction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def axial_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def coefficient_of_friction_method_flash_temperature_method(
        self: "Self",
    ) -> "_1184.ScuffingCoefficientOfFrictionMethods":
        """mastapy.gears.gear_designs.cylindrical.ScuffingCoefficientOfFrictionMethods

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfFrictionMethodFlashTemperatureMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ScuffingCoefficientOfFrictionMethods",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1184",
            "ScuffingCoefficientOfFrictionMethods",
        )(value)

    @property
    @exception_bridge
    def contact_ratio_source(self: "Self") -> "_410.ContactRatioDataSource":
        """mastapy.gears.ContactRatioDataSource

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactRatioSource")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.ContactRatioDataSource"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._410", "ContactRatioDataSource"
        )(value)

    @property
    @exception_bridge
    def duration(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Duration")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def effective_arithmetic_mean_roughness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveArithmeticMeanRoughness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def effective_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elasticity_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticityFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def equivalent_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EquivalentMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_load_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceLoadFactorContact")

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
    def gear_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def line_of_action_parameter_of_maximum_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LineOfActionParameterOfMaximumFlashTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_case(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def load_sharing_factor_of_maximum_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadSharingFactorOfMaximumFlashTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_dynamic_viscosity_at_tooth_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LubricantDynamicViscosityAtToothTemperature"
        )

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
    def mean_coefficient_of_friction_of_maximum_flash_temperature(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanCoefficientOfFrictionOfMaximumFlashTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_dynamic_factor_for_wind_turbine_applications(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumDynamicFactorForWindTurbineApplications"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_face_load_factor_for_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumFaceLoadFactorForContactStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def misalignment_source(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentSource")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def nominal_axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalAxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_radial_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalRadialLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_tangential_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalTangentialLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_transverse_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalTransverseLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def operating_normal_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingNormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_roll_angle_at_highest_point_of_single_tooth_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionRollAngleAtHighestPointOfSingleToothContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_line_velocity_at_operating_pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PitchLineVelocityAtOperatingPitchDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_separating_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialSeparatingLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reduced_modulus_of_elasticity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReducedModulusOfElasticity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def roll_angle_of_maximum_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RollAngleOfMaximumFlashTemperature"
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
    def signed_gear_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedGearRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def slideto_roll_ratio_at_end_of_active_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidetoRollRatioAtEndOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def slideto_roll_ratio_at_pitch_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidetoRollRatioAtPitchPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def slideto_roll_ratio_at_start_of_active_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidetoRollRatioAtStartOfActiveProfile"
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
    def tangential_velocity_at_reference_cylinder(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TangentialVelocityAtReferenceCylinder"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transmitted_tangential_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmittedTangentialLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseContactRatio")

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
    def user_specified_coefficient_of_friction_flash_temperature_method(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UserSpecifiedCoefficientOfFrictionFlashTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def virtual_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def welding_structural_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WeldingStructuralFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubrication_detail(self: "Self") -> "_356.LubricationDetail":
        """mastapy.materials.LubricationDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricationDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rating_settings(
        self: "Self",
    ) -> "_545.CylindricalGearDesignAndRatingSettingsItem":
        """mastapy.gears.rating.cylindrical.CylindricalGearDesignAndRatingSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing(self: "Self") -> "_1183.Scuffing":
        """mastapy.gears.gear_designs.cylindrical.Scuffing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Scuffing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sorted_scuffing_results(self: "Self") -> "_553.CylindricalGearScuffingResults":
        """mastapy.gears.rating.cylindrical.CylindricalGearScuffingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SortedScuffingResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sorted_scuffing_results_without_special_values(
        self: "Self",
    ) -> "_553.CylindricalGearScuffingResults":
        """mastapy.gears.rating.cylindrical.CylindricalGearScuffingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SortedScuffingResultsWithoutSpecialValues"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_556.CylindricalGearSingleFlankRating]":
        """List[mastapy.gears.rating.cylindrical.CylindricalGearSingleFlankRating]

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
    def cast_to(self: "Self") -> "_Cast_CylindricalMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_CylindricalMeshSingleFlankRating
        """
        return _Cast_CylindricalMeshSingleFlankRating(self)
