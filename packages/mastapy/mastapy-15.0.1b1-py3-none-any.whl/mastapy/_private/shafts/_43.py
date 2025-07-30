"""ShaftSettingsItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.shafts import _37
from mastapy._private.utility.databases import _2028

_SHAFT_SETTINGS_ITEM = python_net_import("SMT.MastaAPI.Shafts", "ShaftSettingsItem")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.shafts import _13

    Self = TypeVar("Self", bound="ShaftSettingsItem")
    CastSelf = TypeVar("CastSelf", bound="ShaftSettingsItem._Cast_ShaftSettingsItem")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSettingsItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSettingsItem:
    """Special nested class for casting ShaftSettingsItem to subclasses."""

    __parent__: "ShaftSettingsItem"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def shaft_settings_item(self: "CastSelf") -> "ShaftSettingsItem":
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
class ShaftSettingsItem(_2028.NamedDatabaseItem):
    """ShaftSettingsItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SETTINGS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def create_new_assembly_by_default_when_adding_part_via_dxf(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CreateNewAssemblyByDefaultWhenAddingPartViaDXF"
        )

        if temp is None:
            return False

        return temp

    @create_new_assembly_by_default_when_adding_part_via_dxf.setter
    @exception_bridge
    @enforce_parameter_types
    def create_new_assembly_by_default_when_adding_part_via_dxf(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CreateNewAssemblyByDefaultWhenAddingPartViaDXF",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def reliability_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReliabilityFactor")

        if temp is None:
            return 0.0

        return temp

    @reliability_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def reliability_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReliabilityFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def required_shaft_reliability(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RequiredShaftReliability")

        if temp is None:
            return 0.0

        return temp

    @required_shaft_reliability.setter
    @exception_bridge
    @enforce_parameter_types
    def required_shaft_reliability(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredShaftReliability",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shaft_rating_method(self: "Self") -> "_37.ShaftRatingMethod":
        """mastapy.shafts.ShaftRatingMethod

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftRatingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Shafts.ShaftRatingMethod")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.shafts._37", "ShaftRatingMethod"
        )(value)

    @property
    @exception_bridge
    def shaft_rating_method_selector(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ShaftRatingMethod":
        """EnumWithSelectedValue[mastapy.shafts.ShaftRatingMethod]"""
        temp = pythonnet_property_get(self.wrapped, "ShaftRatingMethodSelector")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ShaftRatingMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @shaft_rating_method_selector.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_rating_method_selector(
        self: "Self", value: "_37.ShaftRatingMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ShaftRatingMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ShaftRatingMethodSelector", value)

    @property
    @exception_bridge
    def version_of_miners_rule(self: "Self") -> "_13.FkmVersionOfMinersRule":
        """mastapy.shafts.FkmVersionOfMinersRule"""
        temp = pythonnet_property_get(self.wrapped, "VersionOfMinersRule")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Shafts.FkmVersionOfMinersRule"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.shafts._13", "FkmVersionOfMinersRule"
        )(value)

    @version_of_miners_rule.setter
    @exception_bridge
    @enforce_parameter_types
    def version_of_miners_rule(
        self: "Self", value: "_13.FkmVersionOfMinersRule"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Shafts.FkmVersionOfMinersRule"
        )
        pythonnet_property_set(self.wrapped, "VersionOfMinersRule", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSettingsItem":
        """Cast to another type.

        Returns:
            _Cast_ShaftSettingsItem
        """
        return _Cast_ShaftSettingsItem(self)
