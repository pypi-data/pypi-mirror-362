"""BevelHypoidGearRatingSettingsItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
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

_BEVEL_HYPOID_GEAR_RATING_SETTINGS_ITEM = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns", "BevelHypoidGearRatingSettingsItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.materials import _707
    from mastapy._private.gears.rating.hypoid import _532
    from mastapy._private.gears.rating.iso_10300 import _511, _519, _526

    Self = TypeVar("Self", bound="BevelHypoidGearRatingSettingsItem")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelHypoidGearRatingSettingsItem._Cast_BevelHypoidGearRatingSettingsItem",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelHypoidGearRatingSettingsItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelHypoidGearRatingSettingsItem:
    """Special nested class for casting BevelHypoidGearRatingSettingsItem to subclasses."""

    __parent__: "BevelHypoidGearRatingSettingsItem"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def bevel_hypoid_gear_rating_settings_item(
        self: "CastSelf",
    ) -> "BevelHypoidGearRatingSettingsItem":
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
class BevelHypoidGearRatingSettingsItem(_2028.NamedDatabaseItem):
    """BevelHypoidGearRatingSettingsItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_HYPOID_GEAR_RATING_SETTINGS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bevel_gear_rating_method(self: "Self") -> "_707.RatingMethods":
        """mastapy.gears.materials.RatingMethods"""
        temp = pythonnet_property_get(self.wrapped, "BevelGearRatingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Materials.RatingMethods"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.materials._707", "RatingMethods"
        )(value)

    @bevel_gear_rating_method.setter
    @exception_bridge
    @enforce_parameter_types
    def bevel_gear_rating_method(self: "Self", value: "_707.RatingMethods") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Materials.RatingMethods"
        )
        pythonnet_property_set(self.wrapped, "BevelGearRatingMethod", value)

    @property
    @exception_bridge
    def bevel_general_load_factors_k_method(
        self: "Self",
    ) -> "_511.GeneralLoadFactorCalculationMethod":
        """mastapy.gears.rating.isoGeneralLoadFactorCalculationMethod"""
        temp = pythonnet_property_get(self.wrapped, "BevelGeneralLoadFactorsKMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Rating.Iso10300.GeneralLoadFactorCalculationMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating._511", "GeneralLoadFactorCalculationMethod"
        )(value)

    @bevel_general_load_factors_k_method.setter
    @exception_bridge
    @enforce_parameter_types
    def bevel_general_load_factors_k_method(
        self: "Self", value: "_511.GeneralLoadFactorCalculationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Rating.Iso10300.GeneralLoadFactorCalculationMethod",
        )
        pythonnet_property_set(self.wrapped, "BevelGeneralLoadFactorsKMethod", value)

    @property
    @exception_bridge
    def bevel_pitting_factor_calculation_method(
        self: "Self",
    ) -> "_526.PittingFactorCalculationMethod":
        """mastapy.gears.rating.isoPittingFactorCalculationMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "BevelPittingFactorCalculationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Iso10300.PittingFactorCalculationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating._526", "PittingFactorCalculationMethod"
        )(value)

    @bevel_pitting_factor_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def bevel_pitting_factor_calculation_method(
        self: "Self", value: "_526.PittingFactorCalculationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Iso10300.PittingFactorCalculationMethod"
        )
        pythonnet_property_set(
            self.wrapped, "BevelPittingFactorCalculationMethod", value
        )

    @property
    @exception_bridge
    def hypoid_gear_rating_method(self: "Self") -> "_532.HypoidRatingMethod":
        """mastapy.gears.rating.hypoid.HypoidRatingMethod"""
        temp = pythonnet_property_get(self.wrapped, "HypoidGearRatingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Hypoid.HypoidRatingMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.hypoid._532", "HypoidRatingMethod"
        )(value)

    @hypoid_gear_rating_method.setter
    @exception_bridge
    @enforce_parameter_types
    def hypoid_gear_rating_method(
        self: "Self", value: "_532.HypoidRatingMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Hypoid.HypoidRatingMethod"
        )
        pythonnet_property_set(self.wrapped, "HypoidGearRatingMethod", value)

    @property
    @exception_bridge
    def hypoid_general_load_factors_k_method(
        self: "Self",
    ) -> "_511.GeneralLoadFactorCalculationMethod":
        """mastapy.gears.rating.isoGeneralLoadFactorCalculationMethod"""
        temp = pythonnet_property_get(self.wrapped, "HypoidGeneralLoadFactorsKMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Rating.Iso10300.GeneralLoadFactorCalculationMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating._511", "GeneralLoadFactorCalculationMethod"
        )(value)

    @hypoid_general_load_factors_k_method.setter
    @exception_bridge
    @enforce_parameter_types
    def hypoid_general_load_factors_k_method(
        self: "Self", value: "_511.GeneralLoadFactorCalculationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Rating.Iso10300.GeneralLoadFactorCalculationMethod",
        )
        pythonnet_property_set(self.wrapped, "HypoidGeneralLoadFactorsKMethod", value)

    @property
    @exception_bridge
    def hypoid_pitting_factor_calculation_method(
        self: "Self",
    ) -> "_526.PittingFactorCalculationMethod":
        """mastapy.gears.rating.isoPittingFactorCalculationMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "HypoidPittingFactorCalculationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Iso10300.PittingFactorCalculationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating._526", "PittingFactorCalculationMethod"
        )(value)

    @hypoid_pitting_factor_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def hypoid_pitting_factor_calculation_method(
        self: "Self", value: "_526.PittingFactorCalculationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Iso10300.PittingFactorCalculationMethod"
        )
        pythonnet_property_set(
            self.wrapped, "HypoidPittingFactorCalculationMethod", value
        )

    @property
    @exception_bridge
    def iso_rating_method_for_bevel_gears(self: "Self") -> "_519.ISO10300RatingMethod":
        """mastapy.gears.rating.isoISO10300RatingMethod"""
        temp = pythonnet_property_get(self.wrapped, "ISORatingMethodForBevelGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Iso10300.ISO10300RatingMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating._519", "ISO10300RatingMethod"
        )(value)

    @iso_rating_method_for_bevel_gears.setter
    @exception_bridge
    @enforce_parameter_types
    def iso_rating_method_for_bevel_gears(
        self: "Self", value: "_519.ISO10300RatingMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Iso10300.ISO10300RatingMethod"
        )
        pythonnet_property_set(self.wrapped, "ISORatingMethodForBevelGears", value)

    @property
    @exception_bridge
    def iso_rating_method_for_hypoid_gears(self: "Self") -> "_519.ISO10300RatingMethod":
        """mastapy.gears.rating.isoISO10300RatingMethod"""
        temp = pythonnet_property_get(self.wrapped, "ISORatingMethodForHypoidGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Iso10300.ISO10300RatingMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating._519", "ISO10300RatingMethod"
        )(value)

    @iso_rating_method_for_hypoid_gears.setter
    @exception_bridge
    @enforce_parameter_types
    def iso_rating_method_for_hypoid_gears(
        self: "Self", value: "_519.ISO10300RatingMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Iso10300.ISO10300RatingMethod"
        )
        pythonnet_property_set(self.wrapped, "ISORatingMethodForHypoidGears", value)

    @property
    @exception_bridge
    def include_mesh_node_misalignments_in_default_report(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeMeshNodeMisalignmentsInDefaultReport"
        )

        if temp is None:
            return False

        return temp

    @include_mesh_node_misalignments_in_default_report.setter
    @exception_bridge
    @enforce_parameter_types
    def include_mesh_node_misalignments_in_default_report(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeMeshNodeMisalignmentsInDefaultReport",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BevelHypoidGearRatingSettingsItem":
        """Cast to another type.

        Returns:
            _Cast_BevelHypoidGearRatingSettingsItem
        """
        return _Cast_BevelHypoidGearRatingSettingsItem(self)
