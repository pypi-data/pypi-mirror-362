"""GearSetManufacturingConfigurationSetup"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEAR_SET_MANUFACTURING_CONFIGURATION_SETUP = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical",
    "GearSetManufacturingConfigurationSetup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.gear_designs.cylindrical import _1106, _1158

    Self = TypeVar("Self", bound="GearSetManufacturingConfigurationSetup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetManufacturingConfigurationSetup._Cast_GearSetManufacturingConfigurationSetup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetManufacturingConfigurationSetup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetManufacturingConfigurationSetup:
    """Special nested class for casting GearSetManufacturingConfigurationSetup to subclasses."""

    __parent__: "GearSetManufacturingConfigurationSetup"

    @property
    def gear_set_manufacturing_configuration_setup(
        self: "CastSelf",
    ) -> "GearSetManufacturingConfigurationSetup":
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
class GearSetManufacturingConfigurationSetup(_0.APIBase):
    """GearSetManufacturingConfigurationSetup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_MANUFACTURING_CONFIGURATION_SETUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def create_new_suitable_cutters(
        self: "Self",
    ) -> "_1106.CreateNewSuitableCutterOption":
        """mastapy.gears.gear_designs.cylindrical.CreateNewSuitableCutterOption"""
        temp = pythonnet_property_get(self.wrapped, "CreateNewSuitableCutters")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CreateNewSuitableCutterOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1106",
            "CreateNewSuitableCutterOption",
        )(value)

    @create_new_suitable_cutters.setter
    @exception_bridge
    @enforce_parameter_types
    def create_new_suitable_cutters(
        self: "Self", value: "_1106.CreateNewSuitableCutterOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CreateNewSuitableCutterOption",
        )
        pythonnet_property_set(self.wrapped, "CreateNewSuitableCutters", value)

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def use_as_design_mode_geometry(
        self: "Self",
    ) -> "_1106.CreateNewSuitableCutterOption":
        """mastapy.gears.gear_designs.cylindrical.CreateNewSuitableCutterOption"""
        temp = pythonnet_property_get(self.wrapped, "UseAsDesignModeGeometry")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CreateNewSuitableCutterOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1106",
            "CreateNewSuitableCutterOption",
        )(value)

    @use_as_design_mode_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def use_as_design_mode_geometry(
        self: "Self", value: "_1106.CreateNewSuitableCutterOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CreateNewSuitableCutterOption",
        )
        pythonnet_property_set(self.wrapped, "UseAsDesignModeGeometry", value)

    @property
    @exception_bridge
    def gears(self: "Self") -> "List[_1158.GearManufacturingConfigSetupViewModel]":
        """List[mastapy.gears.gear_designs.cylindrical.GearManufacturingConfigSetupViewModel]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def cast_to(self: "Self") -> "_Cast_GearSetManufacturingConfigurationSetup":
        """Cast to another type.

        Returns:
            _Cast_GearSetManufacturingConfigurationSetup
        """
        return _Cast_GearSetManufacturingConfigurationSetup(self)
