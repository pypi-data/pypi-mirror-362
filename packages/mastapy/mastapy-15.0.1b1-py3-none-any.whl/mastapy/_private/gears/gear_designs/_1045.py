"""BevelHypoidGearDesignSettingsItem"""

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

_BEVEL_HYPOID_GEAR_DESIGN_SETTINGS_ITEM = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns", "BevelHypoidGearDesignSettingsItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _434

    Self = TypeVar("Self", bound="BevelHypoidGearDesignSettingsItem")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelHypoidGearDesignSettingsItem._Cast_BevelHypoidGearDesignSettingsItem",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelHypoidGearDesignSettingsItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelHypoidGearDesignSettingsItem:
    """Special nested class for casting BevelHypoidGearDesignSettingsItem to subclasses."""

    __parent__: "BevelHypoidGearDesignSettingsItem"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def bevel_hypoid_gear_design_settings_item(
        self: "CastSelf",
    ) -> "BevelHypoidGearDesignSettingsItem":
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
class BevelHypoidGearDesignSettingsItem(_2028.NamedDatabaseItem):
    """BevelHypoidGearDesignSettingsItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_HYPOID_GEAR_DESIGN_SETTINGS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allow_overriding_manufacturing_config_micro_geometry_in_a_load_case(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "AllowOverridingManufacturingConfigMicroGeometryInALoadCase"
        )

        if temp is None:
            return False

        return temp

    @allow_overriding_manufacturing_config_micro_geometry_in_a_load_case.setter
    @exception_bridge
    @enforce_parameter_types
    def allow_overriding_manufacturing_config_micro_geometry_in_a_load_case(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowOverridingManufacturingConfigMicroGeometryInALoadCase",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def minimum_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumRatio")

        if temp is None:
            return 0.0

        return temp

    @minimum_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MinimumRatio", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def quality_grade_type(self: "Self") -> "_434.QualityGradeTypes":
        """mastapy.gears.QualityGradeTypes"""
        temp = pythonnet_property_get(self.wrapped, "QualityGradeType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.QualityGradeTypes")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._434", "QualityGradeTypes"
        )(value)

    @quality_grade_type.setter
    @exception_bridge
    @enforce_parameter_types
    def quality_grade_type(self: "Self", value: "_434.QualityGradeTypes") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Gears.QualityGradeTypes")
        pythonnet_property_set(self.wrapped, "QualityGradeType", value)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelHypoidGearDesignSettingsItem":
        """Cast to another type.

        Returns:
            _Cast_BevelHypoidGearDesignSettingsItem
        """
        return _Cast_BevelHypoidGearDesignSettingsItem(self)
