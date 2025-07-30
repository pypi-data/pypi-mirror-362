"""CylindricalGearCommonFlankMicroGeometry"""

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

_CYLINDRICAL_GEAR_COMMON_FLANK_MICRO_GEOMETRY = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearCommonFlankMicroGeometry",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.gear_designs.cylindrical import _1135

    Self = TypeVar("Self", bound="CylindricalGearCommonFlankMicroGeometry")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearCommonFlankMicroGeometry._Cast_CylindricalGearCommonFlankMicroGeometry",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearCommonFlankMicroGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearCommonFlankMicroGeometry:
    """Special nested class for casting CylindricalGearCommonFlankMicroGeometry to subclasses."""

    __parent__: "CylindricalGearCommonFlankMicroGeometry"

    @property
    def cylindrical_gear_common_flank_micro_geometry(
        self: "CastSelf",
    ) -> "CylindricalGearCommonFlankMicroGeometry":
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
class CylindricalGearCommonFlankMicroGeometry(_0.APIBase):
    """CylindricalGearCommonFlankMicroGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_COMMON_FLANK_MICRO_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def profile_factor_for_0_bias_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileFactorFor0BiasRelief")

        if temp is None:
            return 0.0

        return temp

    @profile_factor_for_0_bias_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_factor_for_0_bias_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileFactorFor0BiasRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def read_micro_geometry_from_an_external_file_using_file_name(
        self: "Self",
    ) -> "str":
        """str"""
        temp = pythonnet_property_get(
            self.wrapped, "ReadMicroGeometryFromAnExternalFileUsingFileName"
        )

        if temp is None:
            return ""

        return temp

    @read_micro_geometry_from_an_external_file_using_file_name.setter
    @exception_bridge
    @enforce_parameter_types
    def read_micro_geometry_from_an_external_file_using_file_name(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReadMicroGeometryFromAnExternalFileUsingFileName",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def use_measured_map_data(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseMeasuredMapData")

        if temp is None:
            return False

        return temp

    @use_measured_map_data.setter
    @exception_bridge
    @enforce_parameter_types
    def use_measured_map_data(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseMeasuredMapData",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def zero_bias_relief(self: "Self") -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZeroBiasRelief")

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
    def read_micro_geometry_from_an_external_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ReadMicroGeometryFromAnExternalFile")

    @exception_bridge
    def switch_measured_data_direction_with_respect_to_face_width(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "SwitchMeasuredDataDirectionWithRespectToFaceWidth"
        )

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
    def cast_to(self: "Self") -> "_Cast_CylindricalGearCommonFlankMicroGeometry":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearCommonFlankMicroGeometry
        """
        return _Cast_CylindricalGearCommonFlankMicroGeometry(self)
