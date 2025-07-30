"""ThermalStator"""

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
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_THERMAL_STATOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "ThermalStator"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.thermal import _1485, _1488
    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _208

    Self = TypeVar("Self", bound="ThermalStator")
    CastSelf = TypeVar("CastSelf", bound="ThermalStator._Cast_ThermalStator")


__docformat__ = "restructuredtext en"
__all__ = ("ThermalStator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalStator:
    """Special nested class for casting ThermalStator to subclasses."""

    __parent__: "ThermalStator"

    @property
    def thermal_stator(self: "CastSelf") -> "ThermalStator":
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
class ThermalStator(_0.APIBase):
    """ThermalStator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_STATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def interlaminate_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "InterlaminateMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @interlaminate_material.setter
    @exception_bridge
    @enforce_parameter_types
    def interlaminate_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "InterlaminateMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def liner_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "LinerMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @liner_material.setter
    @exception_bridge
    @enforce_parameter_types
    def liner_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "LinerMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def liner_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinerThickness")

        if temp is None:
            return 0.0

        return temp

    @liner_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def liner_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LinerThickness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def housing(self: "Self") -> "_1485.ThermalHousing":
        """mastapy.electric_machines.thermal.ThermalHousing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Housing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def liner_to_stator_wedge_interface_gap(self: "Self") -> "_208.InterfaceGap":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.InterfaceGap

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinerToStatorWedgeInterfaceGap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def wedge_to_stator_slot_interface_gap(self: "Self") -> "_208.InterfaceGap":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.InterfaceGap

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WedgeToStatorSlotInterfaceGap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def windings(self: "Self") -> "_1488.ThermalWindings":
        """mastapy.electric_machines.thermal.ThermalWindings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Windings")

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
    def cast_to(self: "Self") -> "_Cast_ThermalStator":
        """Cast to another type.

        Returns:
            _Cast_ThermalStator
        """
        return _Cast_ThermalStator(self)
