"""AlignConnectedComponentOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
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
from mastapy._private.math_utility import _1675, _1676
from mastapy._private.system_model.fe import _2587

_ALIGN_CONNECTED_COMPONENT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "AlignConnectedComponentOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="AlignConnectedComponentOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AlignConnectedComponentOptions._Cast_AlignConnectedComponentOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AlignConnectedComponentOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AlignConnectedComponentOptions:
    """Special nested class for casting AlignConnectedComponentOptions to subclasses."""

    __parent__: "AlignConnectedComponentOptions"

    @property
    def align_connected_component_options(
        self: "CastSelf",
    ) -> "AlignConnectedComponentOptions":
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
class AlignConnectedComponentOptions(_0.APIBase):
    """AlignConnectedComponentOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ALIGN_CONNECTED_COMPONENT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_direction_normal_to_surface(self: "Self") -> "_1676.Axis":
        """mastapy.math_utility.Axis"""
        temp = pythonnet_property_get(self.wrapped, "ComponentDirectionNormalToSurface")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.MathUtility.Axis")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1676", "Axis"
        )(value)

    @component_direction_normal_to_surface.setter
    @exception_bridge
    @enforce_parameter_types
    def component_direction_normal_to_surface(
        self: "Self", value: "_1676.Axis"
    ) -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.MathUtility.Axis")
        pythonnet_property_set(self.wrapped, "ComponentDirectionNormalToSurface", value)

    @property
    @exception_bridge
    def component_orientation(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ComponentOrientationOption":
        """EnumWithSelectedValue[mastapy.system_model.fe.ComponentOrientationOption]"""
        temp = pythonnet_property_get(self.wrapped, "ComponentOrientation")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ComponentOrientationOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @component_orientation.setter
    @exception_bridge
    @enforce_parameter_types
    def component_orientation(
        self: "Self", value: "_2587.ComponentOrientationOption"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ComponentOrientationOption.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ComponentOrientation", value)

    @property
    @exception_bridge
    def fe_axis_approximately_in_perpendicular_direction(
        self: "Self",
    ) -> "_1675.AlignmentAxis":
        """mastapy.math_utility.AlignmentAxis"""
        temp = pythonnet_property_get(
            self.wrapped, "FEAxisApproximatelyInPerpendicularDirection"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.MathUtility.AlignmentAxis")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1675", "AlignmentAxis"
        )(value)

    @fe_axis_approximately_in_perpendicular_direction.setter
    @exception_bridge
    @enforce_parameter_types
    def fe_axis_approximately_in_perpendicular_direction(
        self: "Self", value: "_1675.AlignmentAxis"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.AlignmentAxis"
        )
        pythonnet_property_set(
            self.wrapped, "FEAxisApproximatelyInPerpendicularDirection", value
        )

    @property
    @exception_bridge
    def first_component_alignment_axis(self: "Self") -> "_1676.Axis":
        """mastapy.math_utility.Axis"""
        temp = pythonnet_property_get(self.wrapped, "FirstComponentAlignmentAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.MathUtility.Axis")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1676", "Axis"
        )(value)

    @first_component_alignment_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def first_component_alignment_axis(self: "Self", value: "_1676.Axis") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.MathUtility.Axis")
        pythonnet_property_set(self.wrapped, "FirstComponentAlignmentAxis", value)

    @property
    @exception_bridge
    def first_fe_alignment_axis(self: "Self") -> "_1675.AlignmentAxis":
        """mastapy.math_utility.AlignmentAxis"""
        temp = pythonnet_property_get(self.wrapped, "FirstFEAlignmentAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.MathUtility.AlignmentAxis")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1675", "AlignmentAxis"
        )(value)

    @first_fe_alignment_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def first_fe_alignment_axis(self: "Self", value: "_1675.AlignmentAxis") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.AlignmentAxis"
        )
        pythonnet_property_set(self.wrapped, "FirstFEAlignmentAxis", value)

    @property
    @exception_bridge
    def perpendicular_component_alignment_axis(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_Axis":
        """EnumWithSelectedValue[mastapy.math_utility.Axis]"""
        temp = pythonnet_property_get(
            self.wrapped, "PerpendicularComponentAlignmentAxis"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_Axis.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @perpendicular_component_alignment_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def perpendicular_component_alignment_axis(
        self: "Self", value: "_1676.Axis"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_Axis.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "PerpendicularComponentAlignmentAxis", value
        )

    @property
    @exception_bridge
    def second_component_alignment_axis(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_Axis":
        """EnumWithSelectedValue[mastapy.math_utility.Axis]"""
        temp = pythonnet_property_get(self.wrapped, "SecondComponentAlignmentAxis")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_Axis.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @second_component_alignment_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def second_component_alignment_axis(self: "Self", value: "_1676.Axis") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_Axis.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "SecondComponentAlignmentAxis", value)

    @property
    @exception_bridge
    def second_fe_alignment_axis(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_AlignmentAxis":
        """EnumWithSelectedValue[mastapy.math_utility.AlignmentAxis]"""
        temp = pythonnet_property_get(self.wrapped, "SecondFEAlignmentAxis")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_AlignmentAxis.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @second_fe_alignment_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def second_fe_alignment_axis(self: "Self", value: "_1675.AlignmentAxis") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_AlignmentAxis.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "SecondFEAlignmentAxis", value)

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
    def align_component(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AlignComponent")

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
    def cast_to(self: "Self") -> "_Cast_AlignConnectedComponentOptions":
        """Cast to another type.

        Returns:
            _Cast_AlignConnectedComponentOptions
        """
        return _Cast_AlignConnectedComponentOptions(self)
