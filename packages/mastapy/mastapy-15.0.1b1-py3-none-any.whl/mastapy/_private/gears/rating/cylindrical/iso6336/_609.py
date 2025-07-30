"""ISO6336AbstractMeshSingleFlankRating"""

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

_ISO6336_ABSTRACT_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "ISO6336AbstractMeshSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating import _457
    from mastapy._private.gears.rating.cylindrical import _569
    from mastapy._private.gears.rating.cylindrical.din3990 import _624
    from mastapy._private.gears.rating.cylindrical.iso6336 import (
        _603,
        _605,
        _607,
        _608,
        _611,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _581,
        _583,
        _585,
    )

    Self = TypeVar("Self", bound="ISO6336AbstractMeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO6336AbstractMeshSingleFlankRating._Cast_ISO6336AbstractMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO6336AbstractMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO6336AbstractMeshSingleFlankRating:
    """Special nested class for casting ISO6336AbstractMeshSingleFlankRating to subclasses."""

    __parent__: "ISO6336AbstractMeshSingleFlankRating"

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
    def iso6336_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "ISO6336AbstractMeshSingleFlankRating":
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
class ISO6336AbstractMeshSingleFlankRating(_558.CylindricalMeshSingleFlankRating):
    """ISO6336AbstractMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO6336_ABSTRACT_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def application_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ApplicationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_load_per_unit_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageLoadPerUnitFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_ratio_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactRatioFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_ratio_factor_for_nominal_root_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactRatioFactorForNominalRootRootStress"
        )

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
    def helix_angle_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngleFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_angle_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngleFactorContact")

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
    def misalignment_contact_pattern_enhancement(
        self: "Self",
    ) -> "_569.MisalignmentContactPatternEnhancements":
        """mastapy.gears.rating.cylindrical.MisalignmentContactPatternEnhancements

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MisalignmentContactPatternEnhancement"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Rating.Cylindrical.MisalignmentContactPatternEnhancements",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical._569",
            "MisalignmentContactPatternEnhancements",
        )(value)

    @property
    @exception_bridge
    def nominal_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalContactStress")

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
    def sum_of_tangential_velocities_at_end_of_active_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SumOfTangentialVelocitiesAtEndOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sum_of_tangential_velocities_at_pitch_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SumOfTangentialVelocitiesAtPitchPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sum_of_tangential_velocities_at_start_of_active_profile(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SumOfTangentialVelocitiesAtStartOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_load_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseLoadFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def zone_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZoneFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_608.ISO6336AbstractGearSingleFlankRating]":
        """List[mastapy.gears.rating.cylindrical.iso6336.ISO6336AbstractGearSingleFlankRating]

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
    def isodin_cylindrical_gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_608.ISO6336AbstractGearSingleFlankRating]":
        """List[mastapy.gears.rating.cylindrical.iso6336.ISO6336AbstractGearSingleFlankRating]

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
    def cast_to(self: "Self") -> "_Cast_ISO6336AbstractMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO6336AbstractMeshSingleFlankRating
        """
        return _Cast_ISO6336AbstractMeshSingleFlankRating(self)
