"""CylindricalPlasticGearRatingSettingsItem"""

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
from mastapy._private.utility.databases import _2028

_CYLINDRICAL_PLASTIC_GEAR_RATING_SETTINGS_ITEM = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalPlasticGearRatingSettingsItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalPlasticGearRatingSettingsItem")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalPlasticGearRatingSettingsItem._Cast_CylindricalPlasticGearRatingSettingsItem",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlasticGearRatingSettingsItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalPlasticGearRatingSettingsItem:
    """Special nested class for casting CylindricalPlasticGearRatingSettingsItem to subclasses."""

    __parent__: "CylindricalPlasticGearRatingSettingsItem"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def cylindrical_plastic_gear_rating_settings_item(
        self: "CastSelf",
    ) -> "CylindricalPlasticGearRatingSettingsItem":
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
class CylindricalPlasticGearRatingSettingsItem(_2028.NamedDatabaseItem):
    """CylindricalPlasticGearRatingSettingsItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_PLASTIC_GEAR_RATING_SETTINGS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def use_approximate_value_of_10_for_spiral_helix_angle_factor_for_contact_rating(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "UseApproximateValueOf10ForSpiralHelixAngleFactorForContactRating",
        )

        if temp is None:
            return False

        return temp

    @use_approximate_value_of_10_for_spiral_helix_angle_factor_for_contact_rating.setter
    @exception_bridge
    @enforce_parameter_types
    def use_approximate_value_of_10_for_spiral_helix_angle_factor_for_contact_rating(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseApproximateValueOf10ForSpiralHelixAngleFactorForContactRating",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_approximate_value_of_double_the_normal_module_for_profile_line_length_of_the_active_tooth_flank(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "UseApproximateValueOfDoubleTheNormalModuleForProfileLineLengthOfTheActiveToothFlank",
        )

        if temp is None:
            return False

        return temp

    @use_approximate_value_of_double_the_normal_module_for_profile_line_length_of_the_active_tooth_flank.setter
    @exception_bridge
    @enforce_parameter_types
    def use_approximate_value_of_double_the_normal_module_for_profile_line_length_of_the_active_tooth_flank(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseApproximateValueOfDoubleTheNormalModuleForProfileLineLengthOfTheActiveToothFlank",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalPlasticGearRatingSettingsItem":
        """Cast to another type.

        Returns:
            _Cast_CylindricalPlasticGearRatingSettingsItem
        """
        return _Cast_CylindricalPlasticGearRatingSettingsItem(self)
