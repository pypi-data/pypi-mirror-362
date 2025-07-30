"""AbstractStator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
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
_ABSTRACT_STATOR = python_net_import("SMT.MastaAPI.ElectricMachines", "AbstractStator")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import _1366, _1373, _1435, _1454

    Self = TypeVar("Self", bound="AbstractStator")
    CastSelf = TypeVar("CastSelf", bound="AbstractStator._Cast_AbstractStator")


__docformat__ = "restructuredtext en"
__all__ = ("AbstractStator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractStator:
    """Special nested class for casting AbstractStator to subclasses."""

    __parent__: "AbstractStator"

    @property
    def cad_stator(self: "CastSelf") -> "_1373.CADStator":
        from mastapy._private.electric_machines import _1373

        return self.__parent__._cast(_1373.CADStator)

    @property
    def stator(self: "CastSelf") -> "_1435.Stator":
        from mastapy._private.electric_machines import _1435

        return self.__parent__._cast(_1435.Stator)

    @property
    def abstract_stator(self: "CastSelf") -> "AbstractStator":
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
class AbstractStator(_0.APIBase):
    """AbstractStator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_STATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle_between_stator_partitioning_lines(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "AngleBetweenStatorPartitioningLines"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @angle_between_stator_partitioning_lines.setter
    @exception_bridge
    @enforce_parameter_types
    def angle_between_stator_partitioning_lines(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "AngleBetweenStatorPartitioningLines", value
        )

    @property
    @exception_bridge
    def back_iron_inner_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BackIronInnerRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def back_iron_mid_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BackIronMidRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inner_diameter_of_stator_teeth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerDiameterOfStatorTeeth")

        if temp is None:
            return 0.0

        return temp

    @inner_diameter_of_stator_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_diameter_of_stator_teeth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerDiameterOfStatorTeeth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mid_tooth_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MidToothRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_slots(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfSlots")

        if temp is None:
            return 0

        return temp

    @number_of_slots.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_slots(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfSlots", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def outer_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def split_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SplitRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stator_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StatorLength")

        if temp is None:
            return 0.0

        return temp

    @stator_length.setter
    @exception_bridge
    @enforce_parameter_types
    def stator_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StatorLength", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def stator_material_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "StatorMaterialDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @stator_material_database.setter
    @exception_bridge
    @enforce_parameter_types
    def stator_material_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "StatorMaterialDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def tooth_and_slot(self: "Self") -> "_1366.AbstractToothAndSlot":
        """mastapy.electric_machines.AbstractToothAndSlot

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothAndSlot")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def windings(self: "Self") -> "_1454.Windings":
        """mastapy.electric_machines.Windings

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
    def cast_to(self: "Self") -> "_Cast_AbstractStator":
        """Cast to another type.

        Returns:
            _Cast_AbstractStator
        """
        return _Cast_AbstractStator(self)
