"""DesignSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1778

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_DESIGN_SETTINGS = python_net_import("SMT.MastaAPI.SystemModel", "DesignSettings")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings import _2084
    from mastapy._private.gears.gear_designs import _1045, _1047, _1050
    from mastapy._private.gears.gear_designs.cylindrical import _1124, _1132
    from mastapy._private.gears.rating.cylindrical import _545
    from mastapy._private.materials import _362
    from mastapy._private.nodal_analysis import _53
    from mastapy._private.shafts import _43

    Self = TypeVar("Self", bound="DesignSettings")
    CastSelf = TypeVar("CastSelf", bound="DesignSettings._Cast_DesignSettings")


__docformat__ = "restructuredtext en"
__all__ = ("DesignSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignSettings:
    """Special nested class for casting DesignSettings to subclasses."""

    __parent__: "DesignSettings"

    @property
    def design_settings(self: "CastSelf") -> "DesignSettings":
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
class DesignSettings(_0.APIBase, _1778.IHaveAllSettings):
    """DesignSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def analysis_settings_for_new_designs(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "AnalysisSettingsForNewDesigns", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @analysis_settings_for_new_designs.setter
    @exception_bridge
    @enforce_parameter_types
    def analysis_settings_for_new_designs(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "AnalysisSettingsForNewDesigns",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def bearing_settings_for_new_designs(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "BearingSettingsForNewDesigns", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @bearing_settings_for_new_designs.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_settings_for_new_designs(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "BearingSettingsForNewDesigns",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def bevel_hypoid_gear_design_settings_for_new_designs_database_item(
        self: "Self",
    ) -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped,
            "BevelHypoidGearDesignSettingsForNewDesignsDatabaseItem",
            "SelectedItemName",
        )

        if temp is None:
            return ""

        return temp

    @bevel_hypoid_gear_design_settings_for_new_designs_database_item.setter
    @exception_bridge
    @enforce_parameter_types
    def bevel_hypoid_gear_design_settings_for_new_designs_database_item(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "BevelHypoidGearDesignSettingsForNewDesignsDatabaseItem",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def bevel_hypoid_gear_rating_settings_for_new_designs_database_item(
        self: "Self",
    ) -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped,
            "BevelHypoidGearRatingSettingsForNewDesignsDatabaseItem",
            "SelectedItemName",
        )

        if temp is None:
            return ""

        return temp

    @bevel_hypoid_gear_rating_settings_for_new_designs_database_item.setter
    @exception_bridge
    @enforce_parameter_types
    def bevel_hypoid_gear_rating_settings_for_new_designs_database_item(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "BevelHypoidGearRatingSettingsForNewDesignsDatabaseItem",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def current_analysis_settings(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "CurrentAnalysisSettings", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @current_analysis_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def current_analysis_settings(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CurrentAnalysisSettings",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def current_bearing_settings(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "CurrentBearingSettings", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @current_bearing_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def current_bearing_settings(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CurrentBearingSettings",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def current_bevel_hypoid_gear_design_settings(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "CurrentBevelHypoidGearDesignSettings", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @current_bevel_hypoid_gear_design_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def current_bevel_hypoid_gear_design_settings(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CurrentBevelHypoidGearDesignSettings",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def current_bevel_hypoid_gear_rating_settings(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "CurrentBevelHypoidGearRatingSettings", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @current_bevel_hypoid_gear_rating_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def current_bevel_hypoid_gear_rating_settings(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CurrentBevelHypoidGearRatingSettings",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def current_cylindrical_gear_design_constraints_settings(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped,
            "CurrentCylindricalGearDesignConstraintsSettings",
            "SelectedItemName",
        )

        if temp is None:
            return ""

        return temp

    @current_cylindrical_gear_design_constraints_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def current_cylindrical_gear_design_constraints_settings(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CurrentCylindricalGearDesignConstraintsSettings",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def current_cylindrical_gear_design_and_rating_settings(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped,
            "CurrentCylindricalGearDesignAndRatingSettings",
            "SelectedItemName",
        )

        if temp is None:
            return ""

        return temp

    @current_cylindrical_gear_design_and_rating_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def current_cylindrical_gear_design_and_rating_settings(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CurrentCylindricalGearDesignAndRatingSettings",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def current_cylindrical_gear_micro_geometry_settings(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped,
            "CurrentCylindricalGearMicroGeometrySettings",
            "SelectedItemName",
        )

        if temp is None:
            return ""

        return temp

    @current_cylindrical_gear_micro_geometry_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def current_cylindrical_gear_micro_geometry_settings(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CurrentCylindricalGearMicroGeometrySettings",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def current_design_constraints_settings(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "CurrentDesignConstraintsSettings", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @current_design_constraints_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def current_design_constraints_settings(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CurrentDesignConstraintsSettings",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def current_materials_settings(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "CurrentMaterialsSettings", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @current_materials_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def current_materials_settings(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CurrentMaterialsSettings",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def current_shaft_settings(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "CurrentShaftSettings", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @current_shaft_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def current_shaft_settings(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CurrentShaftSettings",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def cylindrical_gear_design_constraints_settings_for_new_designs(
        self: "Self",
    ) -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped,
            "CylindricalGearDesignConstraintsSettingsForNewDesigns",
            "SelectedItemName",
        )

        if temp is None:
            return ""

        return temp

    @cylindrical_gear_design_constraints_settings_for_new_designs.setter
    @exception_bridge
    @enforce_parameter_types
    def cylindrical_gear_design_constraints_settings_for_new_designs(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CylindricalGearDesignConstraintsSettingsForNewDesigns",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def cylindrical_gear_design_and_rating_settings_for_new_designs(
        self: "Self",
    ) -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped,
            "CylindricalGearDesignAndRatingSettingsForNewDesigns",
            "SelectedItemName",
        )

        if temp is None:
            return ""

        return temp

    @cylindrical_gear_design_and_rating_settings_for_new_designs.setter
    @exception_bridge
    @enforce_parameter_types
    def cylindrical_gear_design_and_rating_settings_for_new_designs(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CylindricalGearDesignAndRatingSettingsForNewDesigns",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def cylindrical_gear_micro_geometry_settings_for_new_designs(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped,
            "CylindricalGearMicroGeometrySettingsForNewDesigns",
            "SelectedItemName",
        )

        if temp is None:
            return ""

        return temp

    @cylindrical_gear_micro_geometry_settings_for_new_designs.setter
    @exception_bridge
    @enforce_parameter_types
    def cylindrical_gear_micro_geometry_settings_for_new_designs(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CylindricalGearMicroGeometrySettingsForNewDesigns",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def design_constraints_settings_for_new_designs(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "DesignConstraintsSettingsForNewDesigns", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @design_constraints_settings_for_new_designs.setter
    @exception_bridge
    @enforce_parameter_types
    def design_constraints_settings_for_new_designs(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "DesignConstraintsSettingsForNewDesigns",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def materials_settings_for_new_designs(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "MaterialsSettingsForNewDesigns", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @materials_settings_for_new_designs.setter
    @exception_bridge
    @enforce_parameter_types
    def materials_settings_for_new_designs(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "MaterialsSettingsForNewDesigns",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def shaft_settings_for_new_designs(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "ShaftSettingsForNewDesigns", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @shaft_settings_for_new_designs.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_settings_for_new_designs(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ShaftSettingsForNewDesigns",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def analysis_settings(self: "Self") -> "_53.AnalysisSettingsItem":
        """mastapy.nodal_analysis.AnalysisSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bearing_settings(self: "Self") -> "_2084.BearingSettingsItem":
        """mastapy.bearings.BearingSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bevel_hypoid_gear_design_settings(
        self: "Self",
    ) -> "_1045.BevelHypoidGearDesignSettingsItem":
        """mastapy.gears.gear_designs.BevelHypoidGearDesignSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelHypoidGearDesignSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bevel_hypoid_gear_rating_settings(
        self: "Self",
    ) -> "_1047.BevelHypoidGearRatingSettingsItem":
        """mastapy.gears.gear_designs.BevelHypoidGearRatingSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelHypoidGearRatingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_design_constraints_settings(
        self: "Self",
    ) -> "_1124.CylindricalGearDesignConstraints":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearDesignConstraintsSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_design_and_rating_settings(
        self: "Self",
    ) -> "_545.CylindricalGearDesignAndRatingSettingsItem":
        """mastapy.gears.rating.cylindrical.CylindricalGearDesignAndRatingSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearDesignAndRatingSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_micro_geometry_settings(
        self: "Self",
    ) -> "_1132.CylindricalGearMicroGeometrySettingsItem":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearMicroGeometrySettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearMicroGeometrySettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def design_constraints_settings(
        self: "Self",
    ) -> "_1050.DesignConstraintsCollection":
        """mastapy.gears.gear_designs.DesignConstraintsCollection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignConstraintsSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def materials_settings(self: "Self") -> "_362.MaterialsSettingsItem":
        """mastapy.materials.MaterialsSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialsSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_settings(self: "Self") -> "_43.ShaftSettingsItem":
        """mastapy.shafts.ShaftSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def copy_settings_from_file(self: "Self", file_name: "PathLike") -> None:
        """Method does not return.

        Args:
            file_name (PathLike)
        """
        file_name = str(file_name)
        pythonnet_method_call(self.wrapped, "CopySettingsFromFile", file_name)

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_DesignSettings":
        """Cast to another type.

        Returns:
            _Cast_DesignSettings
        """
        return _Cast_DesignSettings(self)
