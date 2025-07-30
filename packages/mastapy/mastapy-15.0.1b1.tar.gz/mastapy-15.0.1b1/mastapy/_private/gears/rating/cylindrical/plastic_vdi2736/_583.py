"""PlasticGearVDI2736AbstractMeshSingleFlankRating"""

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
from mastapy._private.gears.rating.cylindrical.iso6336 import _609

_PLASTIC_GEAR_VDI2736_ABSTRACT_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.PlasticVDI2736",
    "PlasticGearVDI2736AbstractMeshSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1200
    from mastapy._private.gears.rating import _457
    from mastapy._private.gears.rating.cylindrical import _558
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _581,
        _582,
        _585,
    )

    Self = TypeVar("Self", bound="PlasticGearVDI2736AbstractMeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlasticGearVDI2736AbstractMeshSingleFlankRating._Cast_PlasticGearVDI2736AbstractMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlasticGearVDI2736AbstractMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlasticGearVDI2736AbstractMeshSingleFlankRating:
    """Special nested class for casting PlasticGearVDI2736AbstractMeshSingleFlankRating to subclasses."""

    __parent__: "PlasticGearVDI2736AbstractMeshSingleFlankRating"

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
    def metal_plastic_or_plastic_metal_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_581.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _581

        return self.__parent__._cast(
            _581.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating
        )

    @property
    def plastic_plastic_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_585.PlasticPlasticVDI2736MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _585

        return self.__parent__._cast(_585.PlasticPlasticVDI2736MeshSingleFlankRating)

    @property
    def plastic_gear_vdi2736_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "PlasticGearVDI2736AbstractMeshSingleFlankRating":
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
class PlasticGearVDI2736AbstractMeshSingleFlankRating(
    _609.ISO6336AbstractMeshSingleFlankRating
):
    """PlasticGearVDI2736AbstractMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLASTIC_GEAR_VDI2736_ABSTRACT_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def air_temperature_ambient_and_assembly(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AirTemperatureAmbientAndAssembly")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def coefficient_of_friction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFriction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def degree_of_tooth_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DegreeOfToothLoss")

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
    def factor_for_tooth_flank_loading(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FactorForToothFlankLoading")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def factor_for_tooth_root_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FactorForToothRootLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def heat_dissipating_surface_of_housing(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeatDissipatingSurfaceOfHousing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def heat_transfer_resistance_of_housing(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeatTransferResistanceOfHousing")

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
    def percentage_of_openings_in_the_housing_surface(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PercentageOfOpeningsInTheHousingSurface"
        )

        if temp is None:
            return 0.0

        return temp

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
    def relative_tooth_engagement_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeToothEngagementTime")

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
    def type_of_mechanism_housing(self: "Self") -> "_1200.TypeOfMechanismHousing":
        """mastapy.gears.gear_designs.cylindrical.TypeOfMechanismHousing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TypeOfMechanismHousing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.TypeOfMechanismHousing"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1200",
            "TypeOfMechanismHousing",
        )(value)

    @property
    @exception_bridge
    def wear_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WearCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def isodin_cylindrical_gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_582.PlasticGearVDI2736AbstractGearSingleFlankRating]":
        """List[mastapy.gears.rating.cylindrical.plastic_vdi2736.PlasticGearVDI2736AbstractGearSingleFlankRating]

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
    @exception_bridge
    def plastic_vdi2736_cylindrical_gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_582.PlasticGearVDI2736AbstractGearSingleFlankRating]":
        """List[mastapy.gears.rating.cylindrical.plastic_vdi2736.PlasticGearVDI2736AbstractGearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PlasticVDI2736CylindricalGearSingleFlankRatings"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_PlasticGearVDI2736AbstractMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_PlasticGearVDI2736AbstractMeshSingleFlankRating
        """
        return _Cast_PlasticGearVDI2736AbstractMeshSingleFlankRating(self)
