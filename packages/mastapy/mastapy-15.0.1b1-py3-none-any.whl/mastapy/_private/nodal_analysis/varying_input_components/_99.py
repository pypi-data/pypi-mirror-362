"""AbstractVaryingInputComponent"""

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
from mastapy._private.nodal_analysis import _97
from mastapy._private.nodal_analysis.varying_input_components import _104

_ABSTRACT_VARYING_INPUT_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.VaryingInputComponents", "AbstractVaryingInputComponent"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.math_utility import _1718
    from mastapy._private.math_utility.measured_data import _1749
    from mastapy._private.nodal_analysis.varying_input_components import (
        _100,
        _101,
        _102,
        _103,
        _105,
    )

    Self = TypeVar("Self", bound="AbstractVaryingInputComponent")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractVaryingInputComponent._Cast_AbstractVaryingInputComponent",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractVaryingInputComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractVaryingInputComponent:
    """Special nested class for casting AbstractVaryingInputComponent to subclasses."""

    __parent__: "AbstractVaryingInputComponent"

    @property
    def angle_input_component(self: "CastSelf") -> "_100.AngleInputComponent":
        from mastapy._private.nodal_analysis.varying_input_components import _100

        return self.__parent__._cast(_100.AngleInputComponent)

    @property
    def force_input_component(self: "CastSelf") -> "_101.ForceInputComponent":
        from mastapy._private.nodal_analysis.varying_input_components import _101

        return self.__parent__._cast(_101.ForceInputComponent)

    @property
    def moment_input_component(self: "CastSelf") -> "_102.MomentInputComponent":
        from mastapy._private.nodal_analysis.varying_input_components import _102

        return self.__parent__._cast(_102.MomentInputComponent)

    @property
    def non_dimensional_input_component(
        self: "CastSelf",
    ) -> "_103.NonDimensionalInputComponent":
        from mastapy._private.nodal_analysis.varying_input_components import _103

        return self.__parent__._cast(_103.NonDimensionalInputComponent)

    @property
    def velocity_input_component(self: "CastSelf") -> "_105.VelocityInputComponent":
        from mastapy._private.nodal_analysis.varying_input_components import _105

        return self.__parent__._cast(_105.VelocityInputComponent)

    @property
    def abstract_varying_input_component(
        self: "CastSelf",
    ) -> "AbstractVaryingInputComponent":
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
class AbstractVaryingInputComponent(_0.APIBase):
    """AbstractVaryingInputComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_VARYING_INPUT_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def include_values_before_zero_time(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeValuesBeforeZeroTime")

        if temp is None:
            return False

        return temp

    @include_values_before_zero_time.setter
    @exception_bridge
    @enforce_parameter_types
    def include_values_before_zero_time(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeValuesBeforeZeroTime",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def input_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ValueInputOption":
        """EnumWithSelectedValue[mastapy.nodal_analysis.ValueInputOption]"""
        temp = pythonnet_property_get(self.wrapped, "InputType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ValueInputOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @input_type.setter
    @exception_bridge
    @enforce_parameter_types
    def input_type(self: "Self", value: "_97.ValueInputOption") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ValueInputOption.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "InputType", value)

    @property
    @exception_bridge
    def single_point_selection_method_for_value_vs_time(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_SinglePointSelectionMethod":
        """EnumWithSelectedValue[mastapy.nodal_analysis.varying_input_components.SinglePointSelectionMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "SinglePointSelectionMethodForValueVsTime"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_SinglePointSelectionMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @single_point_selection_method_for_value_vs_time.setter
    @exception_bridge
    @enforce_parameter_types
    def single_point_selection_method_for_value_vs_time(
        self: "Self", value: "_104.SinglePointSelectionMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_SinglePointSelectionMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "SinglePointSelectionMethodForValueVsTime", value
        )

    @property
    @exception_bridge
    def time_profile_repeats(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "TimeProfileRepeats")

        if temp is None:
            return False

        return temp

    @time_profile_repeats.setter
    @exception_bridge
    @enforce_parameter_types
    def time_profile_repeats(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TimeProfileRepeats",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def value_vs_angle(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "ValueVsAngle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @value_vs_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def value_vs_angle(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "ValueVsAngle", value.wrapped)

    @property
    @exception_bridge
    def value_vs_angle_and_speed(self: "Self") -> "_1749.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "ValueVsAngleAndSpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @value_vs_angle_and_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def value_vs_angle_and_speed(
        self: "Self", value: "_1749.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "ValueVsAngleAndSpeed", value.wrapped)

    @property
    @exception_bridge
    def value_vs_position(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "ValueVsPosition")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @value_vs_position.setter
    @exception_bridge
    @enforce_parameter_types
    def value_vs_position(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "ValueVsPosition", value.wrapped)

    @property
    @exception_bridge
    def value_vs_time(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "ValueVsTime")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @value_vs_time.setter
    @exception_bridge
    @enforce_parameter_types
    def value_vs_time(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "ValueVsTime", value.wrapped)

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
    def cast_to(self: "Self") -> "_Cast_AbstractVaryingInputComponent":
        """Cast to another type.

        Returns:
            _Cast_AbstractVaryingInputComponent
        """
        return _Cast_AbstractVaryingInputComponent(self)
