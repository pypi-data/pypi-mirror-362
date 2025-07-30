"""PlasticGearVDI2736AbstractGearSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.rating.cylindrical.iso6336 import _608

_PLASTIC_GEAR_VDI2736_ABSTRACT_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.PlasticVDI2736",
    "PlasticGearVDI2736AbstractGearSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.rating import _455
    from mastapy._private.gears.rating.cylindrical import _556
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _586,
        _587,
        _588,
    )
    from mastapy._private.materials import _374, _375

    Self = TypeVar("Self", bound="PlasticGearVDI2736AbstractGearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlasticGearVDI2736AbstractGearSingleFlankRating._Cast_PlasticGearVDI2736AbstractGearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlasticGearVDI2736AbstractGearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlasticGearVDI2736AbstractGearSingleFlankRating:
    """Special nested class for casting PlasticGearVDI2736AbstractGearSingleFlankRating to subclasses."""

    __parent__: "PlasticGearVDI2736AbstractGearSingleFlankRating"

    @property
    def iso6336_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_608.ISO6336AbstractGearSingleFlankRating":
        return self.__parent__._cast(_608.ISO6336AbstractGearSingleFlankRating)

    @property
    def cylindrical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_556.CylindricalGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _556

        return self.__parent__._cast(_556.CylindricalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_455.GearSingleFlankRating":
        from mastapy._private.gears.rating import _455

        return self.__parent__._cast(_455.GearSingleFlankRating)

    @property
    def plastic_vdi2736_gear_single_flank_rating_in_a_metal_plastic_or_a_plastic_metal_mesh(
        self: "CastSelf",
    ) -> "_587.PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _587

        return self.__parent__._cast(
            _587.PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh
        )

    @property
    def plastic_vdi2736_gear_single_flank_rating_in_a_plastic_plastic_mesh(
        self: "CastSelf",
    ) -> "_588.PlasticVDI2736GearSingleFlankRatingInAPlasticPlasticMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _588

        return self.__parent__._cast(
            _588.PlasticVDI2736GearSingleFlankRatingInAPlasticPlasticMesh
        )

    @property
    def plastic_gear_vdi2736_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "PlasticGearVDI2736AbstractGearSingleFlankRating":
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
class PlasticGearVDI2736AbstractGearSingleFlankRating(
    _608.ISO6336AbstractGearSingleFlankRating
):
    """PlasticGearVDI2736AbstractGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLASTIC_GEAR_VDI2736_ABSTRACT_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_stress_number_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableStressNumberBending")

        if temp is None:
            return 0.0

        return temp

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
    def averaged_linear_wear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AveragedLinearWear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def flank_heat_transfer_coefficient(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlankHeatTransferCoefficient")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def flank_temperature(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FlankTemperature")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @flank_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def flank_temperature(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FlankTemperature", value)

    @property
    @exception_bridge
    def important_note_on_contact_durability_of_pom(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ImportantNoteOnContactDurabilityOfPOM"
        )

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def minimum_factor_of_safety_bending_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumFactorOfSafetyBendingFatigue"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_factor_of_safety_pitting_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumFactorOfSafetyPittingFatigue"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_factor_of_safety_wear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumFactorOfSafetyWear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_tooth_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalToothRootStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_tooth_root_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleToothRootBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitting_stress_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PittingStressLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def profile_line_length_of_the_active_tooth_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileLineLengthOfTheActiveToothFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_heat_transfer_coefficient(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootHeatTransferCoefficient")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def root_temperature(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RootTemperature")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @root_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def root_temperature(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RootTemperature", value)

    @property
    @exception_bridge
    def tooth_root_stress_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothRootStressLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def standard_plastic_sn_curve_for_the_specified_operating_conditions(
        self: "Self",
    ) -> "_586.PlasticSNCurveForTheSpecifiedOperatingConditions":
        """mastapy.gears.rating.cylindrical.plastic_vdi2736.PlasticSNCurveForTheSpecifiedOperatingConditions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StandardPlasticSNCurveForTheSpecifiedOperatingConditions"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bending_stress_cycle_data_for_damage_tables(
        self: "Self",
    ) -> "List[_374.StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]":
        """List[mastapy.materials.StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BendingStressCycleDataForDamageTables"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_stress_cycle_data_for_damage_tables(
        self: "Self",
    ) -> "List[_375.StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]":
        """List[mastapy.materials.StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactStressCycleDataForDamageTables"
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
    ) -> "_Cast_PlasticGearVDI2736AbstractGearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_PlasticGearVDI2736AbstractGearSingleFlankRating
        """
        return _Cast_PlasticGearVDI2736AbstractGearSingleFlankRating(self)
