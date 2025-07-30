"""StatorCutoutSpecification"""

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

_STATOR_CUTOUT_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "StatorCutoutSpecification"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="StatorCutoutSpecification")
    CastSelf = TypeVar(
        "CastSelf", bound="StatorCutoutSpecification._Cast_StatorCutoutSpecification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StatorCutoutSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StatorCutoutSpecification:
    """Special nested class for casting StatorCutoutSpecification to subclasses."""

    __parent__: "StatorCutoutSpecification"

    @property
    def stator_cutout_specification(self: "CastSelf") -> "StatorCutoutSpecification":
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
class StatorCutoutSpecification(_0.APIBase):
    """StatorCutoutSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATOR_CUTOUT_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle_to_first_cutout(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngleToFirstCutout")

        if temp is None:
            return 0.0

        return temp

    @angle_to_first_cutout.setter
    @exception_bridge
    @enforce_parameter_types
    def angle_to_first_cutout(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AngleToFirstCutout",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def corner_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CornerRadius")

        if temp is None:
            return 0.0

        return temp

    @corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def corner_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CornerRadius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def is_cooling_channel(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsCoolingChannel")

        if temp is None:
            return False

        return temp

    @is_cooling_channel.setter
    @exception_bridge
    @enforce_parameter_types
    def is_cooling_channel(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsCoolingChannel",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @exception_bridge
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

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
    def number_of_cutouts(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCutouts")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_cutouts.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_cutouts(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfCutouts", value)

    @property
    @exception_bridge
    def radial_position(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialPosition")

        if temp is None:
            return 0.0

        return temp

    @radial_position.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_position(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialPosition", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def rotation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Rotation")

        if temp is None:
            return 0.0

        return temp

    @rotation.setter
    @exception_bridge
    @enforce_parameter_types
    def rotation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Rotation", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
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
    def cast_to(self: "Self") -> "_Cast_StatorCutoutSpecification":
        """Cast to another type.

        Returns:
            _Cast_StatorCutoutSpecification
        """
        return _Cast_StatorCutoutSpecification(self)
