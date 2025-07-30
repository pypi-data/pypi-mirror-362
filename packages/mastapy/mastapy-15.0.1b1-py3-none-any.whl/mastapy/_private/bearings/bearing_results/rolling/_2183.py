"""ISO14179SettingsPerBearingType"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1779

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_ISO14179_SETTINGS_PER_BEARING_TYPE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "ISO14179SettingsPerBearingType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2099
    from mastapy._private.bearings.bearing_results.rolling import _2181

    Self = TypeVar("Self", bound="ISO14179SettingsPerBearingType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO14179SettingsPerBearingType._Cast_ISO14179SettingsPerBearingType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO14179SettingsPerBearingType",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO14179SettingsPerBearingType:
    """Special nested class for casting ISO14179SettingsPerBearingType to subclasses."""

    __parent__: "ISO14179SettingsPerBearingType"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def iso14179_settings_per_bearing_type(
        self: "CastSelf",
    ) -> "ISO14179SettingsPerBearingType":
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
class ISO14179SettingsPerBearingType(
    _1779.IndependentReportablePropertiesBase["ISO14179SettingsPerBearingType"]
):
    """ISO14179SettingsPerBearingType

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO14179_SETTINGS_PER_BEARING_TYPE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def iso14179_settings_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "ISO14179SettingsDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @iso14179_settings_database.setter
    @exception_bridge
    @enforce_parameter_types
    def iso14179_settings_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ISO14179SettingsDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def rolling_bearing_type(self: "Self") -> "_2099.RollingBearingType":
        """mastapy.bearings.RollingBearingType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingBearingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.RollingBearingType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2099", "RollingBearingType"
        )(value)

    @property
    @exception_bridge
    def iso14179_settings(self: "Self") -> "_2181.ISO14179Settings":
        """mastapy.bearings.bearing_results.rolling.ISO14179Settings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO14179Settings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ISO14179SettingsPerBearingType":
        """Cast to another type.

        Returns:
            _Cast_ISO14179SettingsPerBearingType
        """
        return _Cast_ISO14179SettingsPerBearingType(self)
