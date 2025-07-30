"""RigidConnectorToothLocation"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_RIGID_CONNECTOR_TOOTH_LOCATION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RigidConnectorToothLocation"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="RigidConnectorToothLocation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RigidConnectorToothLocation._Cast_RigidConnectorToothLocation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RigidConnectorToothLocation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RigidConnectorToothLocation:
    """Special nested class for casting RigidConnectorToothLocation to subclasses."""

    __parent__: "RigidConnectorToothLocation"

    @property
    def rigid_connector_tooth_location(
        self: "CastSelf",
    ) -> "RigidConnectorToothLocation":
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
class RigidConnectorToothLocation(_0.APIBase):
    """RigidConnectorToothLocation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RIGID_CONNECTOR_TOOTH_LOCATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def centre_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CentreAngle")

        if temp is None:
            return 0.0

        return temp

    @centre_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def centre_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CentreAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def end_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EndAngle")

        if temp is None:
            return 0.0

        return temp

    @end_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def end_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EndAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def extent(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Extent")

        if temp is None:
            return 0.0

        return temp

    @extent.setter
    @exception_bridge
    @enforce_parameter_types
    def extent(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Extent", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ID")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def major_diameter_error(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MajorDiameterError")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @major_diameter_error.setter
    @exception_bridge
    @enforce_parameter_types
    def major_diameter_error(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MajorDiameterError", value)

    @property
    @exception_bridge
    def major_diameter_radial_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MajorDiameterRadialClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minor_diameter_error(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinorDiameterError")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minor_diameter_error.setter
    @exception_bridge
    @enforce_parameter_types
    def minor_diameter_error(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinorDiameterError", value)

    @property
    @exception_bridge
    def minor_diameter_radial_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinorDiameterRadialClearance")

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
    def normal_clearance_left_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalClearanceLeftFlank")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_clearance_right_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalClearanceRightFlank")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_error_left_flank(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PitchErrorLeftFlank")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pitch_error_left_flank.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_error_left_flank(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PitchErrorLeftFlank", value)

    @property
    @exception_bridge
    def pitch_error_right_flank(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PitchErrorRightFlank")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pitch_error_right_flank.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_error_right_flank(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PitchErrorRightFlank", value)

    @property
    @exception_bridge
    def start_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartAngle")

        if temp is None:
            return 0.0

        return temp

    @start_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def start_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StartAngle", float(value) if value is not None else 0.0
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
    def cast_to(self: "Self") -> "_Cast_RigidConnectorToothLocation":
        """Cast to another type.

        Returns:
            _Cast_RigidConnectorToothLocation
        """
        return _Cast_RigidConnectorToothLocation(self)
