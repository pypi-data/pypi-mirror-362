"""PlungeShaverInputsAndMicroGeometry"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
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
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import _748, _749

_PLUNGE_SHAVER_INPUTS_AND_MICRO_GEOMETRY = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving",
    "PlungeShaverInputsAndMicroGeometry",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import _756

    Self = TypeVar("Self", bound="PlungeShaverInputsAndMicroGeometry")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlungeShaverInputsAndMicroGeometry._Cast_PlungeShaverInputsAndMicroGeometry",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlungeShaverInputsAndMicroGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlungeShaverInputsAndMicroGeometry:
    """Special nested class for casting PlungeShaverInputsAndMicroGeometry to subclasses."""

    __parent__: "PlungeShaverInputsAndMicroGeometry"

    @property
    def plunge_shaver_inputs_and_micro_geometry(
        self: "CastSelf",
    ) -> "PlungeShaverInputsAndMicroGeometry":
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
class PlungeShaverInputsAndMicroGeometry(_0.APIBase):
    """PlungeShaverInputsAndMicroGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLUNGE_SHAVER_INPUTS_AND_MICRO_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def do_both_flanks_have_the_same_micro_geometry(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "DoBothFlanksHaveTheSameMicroGeometry"
        )

        if temp is None:
            return False

        return temp

    @do_both_flanks_have_the_same_micro_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def do_both_flanks_have_the_same_micro_geometry(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DoBothFlanksHaveTheSameMicroGeometry",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def lead_measurement_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod":
        """EnumWithSelectedValue[mastapy.gears.manufacturing.cylindrical.plunge_shaving.MicroGeometryDefinitionMethod]"""
        temp = pythonnet_property_get(self.wrapped, "LeadMeasurementMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @lead_measurement_method.setter
    @exception_bridge
    @enforce_parameter_types
    def lead_measurement_method(
        self: "Self", value: "_748.MicroGeometryDefinitionMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "LeadMeasurementMethod", value)

    @property
    @exception_bridge
    def micro_geometry_source(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionType":
        """EnumWithSelectedValue[mastapy.gears.manufacturing.cylindrical.plunge_shaving.MicroGeometryDefinitionType]"""
        temp = pythonnet_property_get(self.wrapped, "MicroGeometrySource")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @micro_geometry_source.setter
    @exception_bridge
    @enforce_parameter_types
    def micro_geometry_source(
        self: "Self", value: "_749.MicroGeometryDefinitionType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "MicroGeometrySource", value)

    @property
    @exception_bridge
    def number_of_points_of_interest(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPointsOfInterest")

        if temp is None:
            return 0

        return temp

    @number_of_points_of_interest.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_of_interest(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPointsOfInterest",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def profile_measurement_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod":
        """EnumWithSelectedValue[mastapy.gears.manufacturing.cylindrical.plunge_shaving.MicroGeometryDefinitionMethod]"""
        temp = pythonnet_property_get(self.wrapped, "ProfileMeasurementMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @profile_measurement_method.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_measurement_method(
        self: "Self", value: "_748.MicroGeometryDefinitionMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ProfileMeasurementMethod", value)

    @property
    @exception_bridge
    def points_of_interest_left_flank(self: "Self") -> "List[_756.PointOfInterest]":
        """List[mastapy.gears.manufacturing.cylindrical.plunge_shaving.PointOfInterest]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointsOfInterestLeftFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def points_of_interest_right_flank(self: "Self") -> "List[_756.PointOfInterest]":
        """List[mastapy.gears.manufacturing.cylindrical.plunge_shaving.PointOfInterest]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointsOfInterestRightFlank")

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
    def cast_to(self: "Self") -> "_Cast_PlungeShaverInputsAndMicroGeometry":
        """Cast to another type.

        Returns:
            _Cast_PlungeShaverInputsAndMicroGeometry
        """
        return _Cast_PlungeShaverInputsAndMicroGeometry(self)
