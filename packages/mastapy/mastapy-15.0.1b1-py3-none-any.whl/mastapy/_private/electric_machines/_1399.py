"""FieldWindingSpecificationBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
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
_FIELD_WINDING_SPECIFICATION_BASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "FieldWindingSpecificationBase"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import _1369, _1398

    Self = TypeVar("Self", bound="FieldWindingSpecificationBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FieldWindingSpecificationBase._Cast_FieldWindingSpecificationBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FieldWindingSpecificationBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FieldWindingSpecificationBase:
    """Special nested class for casting FieldWindingSpecificationBase to subclasses."""

    __parent__: "FieldWindingSpecificationBase"

    @property
    def cad_field_winding_specification(
        self: "CastSelf",
    ) -> "_1369.CADFieldWindingSpecification":
        from mastapy._private.electric_machines import _1369

        return self.__parent__._cast(_1369.CADFieldWindingSpecification)

    @property
    def field_winding_specification(
        self: "CastSelf",
    ) -> "_1398.FieldWindingSpecification":
        from mastapy._private.electric_machines import _1398

        return self.__parent__._cast(_1398.FieldWindingSpecification)

    @property
    def field_winding_specification_base(
        self: "CastSelf",
    ) -> "FieldWindingSpecificationBase":
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
class FieldWindingSpecificationBase(_0.APIBase):
    """FieldWindingSpecificationBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FIELD_WINDING_SPECIFICATION_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def coil_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoilPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def end_winding_pole_pitch_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EndWindingPolePitchFactor")

        if temp is None:
            return 0.0

        return temp

    @end_winding_pole_pitch_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def end_winding_pole_pitch_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EndWindingPolePitchFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def fill_factor_windings(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FillFactorWindings")

        if temp is None:
            return 0.0

        return temp

    @fill_factor_windings.setter
    @exception_bridge
    @enforce_parameter_types
    def fill_factor_windings(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FillFactorWindings",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def material_cost(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialCost")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_length_per_turn(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanLengthPerTurn")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def number_of_turns(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTurns")

        if temp is None:
            return 0

        return temp

    @number_of_turns.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_turns(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTurns", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def total_length_of_conductors_in_pole(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalLengthOfConductorsInPole")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def winding_material_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindingMaterialArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def winding_material_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "WindingMaterialDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @winding_material_database.setter
    @exception_bridge
    @enforce_parameter_types
    def winding_material_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "WindingMaterialDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

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
    def cast_to(self: "Self") -> "_Cast_FieldWindingSpecificationBase":
        """Cast to another type.

        Returns:
            _Cast_FieldWindingSpecificationBase
        """
        return _Cast_FieldWindingSpecificationBase(self)
