"""RollingBearingFrictionCoefficients"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1779

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_ROLLING_BEARING_FRICTION_COEFFICIENTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "RollingBearingFrictionCoefficients"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2151
    from mastapy._private.bearings.bearing_results.rolling import _2181

    Self = TypeVar("Self", bound="RollingBearingFrictionCoefficients")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RollingBearingFrictionCoefficients._Cast_RollingBearingFrictionCoefficients",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollingBearingFrictionCoefficients",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollingBearingFrictionCoefficients:
    """Special nested class for casting RollingBearingFrictionCoefficients to subclasses."""

    __parent__: "RollingBearingFrictionCoefficients"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def rolling_bearing_friction_coefficients(
        self: "CastSelf",
    ) -> "RollingBearingFrictionCoefficients":
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
class RollingBearingFrictionCoefficients(
    _1779.IndependentReportablePropertiesBase["RollingBearingFrictionCoefficients"]
):
    """RollingBearingFrictionCoefficients

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLING_BEARING_FRICTION_COEFFICIENTS

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
    def use_user_specified_f0(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseUserSpecifiedF0")

        if temp is None:
            return False

        return temp

    @use_user_specified_f0.setter
    @exception_bridge
    @enforce_parameter_types
    def use_user_specified_f0(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseUserSpecifiedF0",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_user_specified_f0r(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseUserSpecifiedF0r")

        if temp is None:
            return False

        return temp

    @use_user_specified_f0r.setter
    @exception_bridge
    @enforce_parameter_types
    def use_user_specified_f0r(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseUserSpecifiedF0r",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_user_specified_f1_for_din7322010(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseUserSpecifiedF1ForDIN7322010")

        if temp is None:
            return False

        return temp

    @use_user_specified_f1_for_din7322010.setter
    @exception_bridge
    @enforce_parameter_types
    def use_user_specified_f1_for_din7322010(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseUserSpecifiedF1ForDIN7322010",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_user_specified_f1r(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseUserSpecifiedF1r")

        if temp is None:
            return False

        return temp

    @use_user_specified_f1r.setter
    @exception_bridge
    @enforce_parameter_types
    def use_user_specified_f1r(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseUserSpecifiedF1r",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def user_specified_f0(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedF0")

        if temp is None:
            return 0.0

        return temp

    @user_specified_f0.setter
    @exception_bridge
    @enforce_parameter_types
    def user_specified_f0(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "UserSpecifiedF0", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def user_specified_f0r(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedF0r")

        if temp is None:
            return 0.0

        return temp

    @user_specified_f0r.setter
    @exception_bridge
    @enforce_parameter_types
    def user_specified_f0r(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "UserSpecifiedF0r", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def user_specified_f1_for_din7322010(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedF1ForDIN7322010")

        if temp is None:
            return 0.0

        return temp

    @user_specified_f1_for_din7322010.setter
    @exception_bridge
    @enforce_parameter_types
    def user_specified_f1_for_din7322010(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserSpecifiedF1ForDIN7322010",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def user_specified_f1r(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedF1r")

        if temp is None:
            return 0.0

        return temp

    @user_specified_f1r.setter
    @exception_bridge
    @enforce_parameter_types
    def user_specified_f1r(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "UserSpecifiedF1r", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def iso14179_dynamic_equivalent_load_factors(
        self: "Self",
    ) -> "_2151.EquivalentLoadFactors":
        """mastapy.bearings.bearing_results.EquivalentLoadFactors

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO14179DynamicEquivalentLoadFactors"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    @exception_bridge
    def iso14179_static_equivalent_load_factors(
        self: "Self",
    ) -> "_2151.EquivalentLoadFactors":
        """mastapy.bearings.bearing_results.EquivalentLoadFactors

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO14179StaticEquivalentLoadFactors"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RollingBearingFrictionCoefficients":
        """Cast to another type.

        Returns:
            _Cast_RollingBearingFrictionCoefficients
        """
        return _Cast_RollingBearingFrictionCoefficients(self)
