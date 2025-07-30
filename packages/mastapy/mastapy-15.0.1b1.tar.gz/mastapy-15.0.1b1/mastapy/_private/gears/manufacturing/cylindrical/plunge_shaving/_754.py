"""PlungeShaverOutputs"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

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
from mastapy._private.gears.manufacturing.cylindrical import _730
from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import _746

_PLUNGE_SHAVER_OUTPUTS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving", "PlungeShaverOutputs"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import (
        _752,
        _757,
        _760,
    )

    Self = TypeVar("Self", bound="PlungeShaverOutputs")
    CastSelf = TypeVar(
        "CastSelf", bound="PlungeShaverOutputs._Cast_PlungeShaverOutputs"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlungeShaverOutputs",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlungeShaverOutputs:
    """Special nested class for casting PlungeShaverOutputs to subclasses."""

    __parent__: "PlungeShaverOutputs"

    @property
    def real_plunge_shaver_outputs(self: "CastSelf") -> "_757.RealPlungeShaverOutputs":
        from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import _757

        return self.__parent__._cast(_757.RealPlungeShaverOutputs)

    @property
    def virtual_plunge_shaver_outputs(
        self: "CastSelf",
    ) -> "_760.VirtualPlungeShaverOutputs":
        from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import _760

        return self.__parent__._cast(_760.VirtualPlungeShaverOutputs)

    @property
    def plunge_shaver_outputs(self: "CastSelf") -> "PlungeShaverOutputs":
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
class PlungeShaverOutputs(_0.APIBase):
    """PlungeShaverOutputs

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLUNGE_SHAVER_OUTPUTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def chart(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ChartType":
        """EnumWithSelectedValue[mastapy.gears.manufacturing.cylindrical.plunge_shaving.ChartType]"""
        temp = pythonnet_property_get(self.wrapped, "Chart")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ChartType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @chart.setter
    @exception_bridge
    @enforce_parameter_types
    def chart(self: "Self", value: "_746.ChartType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_ChartType.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Chart", value)

    @property
    @exception_bridge
    def difference_between_chart_z_plane(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DifferenceBetweenChartZPlane")

        if temp is None:
            return 0.0

        return temp

    @difference_between_chart_z_plane.setter
    @exception_bridge
    @enforce_parameter_types
    def difference_between_chart_z_plane(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DifferenceBetweenChartZPlane",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_modification_on_conjugate_shaver_chart_left_flank(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileModificationOnConjugateShaverChartLeftFlank"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def profile_modification_on_conjugate_shaver_chart_right_flank(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileModificationOnConjugateShaverChartRightFlank"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def selected_flank(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_Flank":
        """EnumWithSelectedValue[mastapy.gears.manufacturing.cylindrical.Flank]"""
        temp = pythonnet_property_get(self.wrapped, "SelectedFlank")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_Flank.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @selected_flank.setter
    @exception_bridge
    @enforce_parameter_types
    def selected_flank(self: "Self", value: "_730.Flank") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_Flank.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "SelectedFlank", value)

    @property
    @exception_bridge
    def shaved_gear_profile_modification_z_plane(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ShavedGearProfileModificationZPlane"
        )

        if temp is None:
            return 0.0

        return temp

    @shaved_gear_profile_modification_z_plane.setter
    @exception_bridge
    @enforce_parameter_types
    def shaved_gear_profile_modification_z_plane(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShavedGearProfileModificationZPlane",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shaver_profile_modification_z_plane(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaverProfileModificationZPlane")

        if temp is None:
            return 0.0

        return temp

    @shaver_profile_modification_z_plane.setter
    @exception_bridge
    @enforce_parameter_types
    def shaver_profile_modification_z_plane(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaverProfileModificationZPlane",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def calculation_details(self: "Self") -> "_752.PlungeShaverGeneration":
        """mastapy.gears.manufacturing.cylindrical.plunge_shaving.PlungeShaverGeneration

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculationDetails")

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
    def cast_to(self: "Self") -> "_Cast_PlungeShaverOutputs":
        """Cast to another type.

        Returns:
            _Cast_PlungeShaverOutputs
        """
        return _Cast_PlungeShaverOutputs(self)
