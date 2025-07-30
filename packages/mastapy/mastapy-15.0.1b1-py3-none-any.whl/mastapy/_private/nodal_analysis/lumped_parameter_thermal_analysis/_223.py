"""UserDefinedHeatTransferCoefficient"""

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
from mastapy._private.math_utility import _1694
from mastapy._private.utility.enums import _2017

_USER_DEFINED_HEAT_TRANSFER_COEFFICIENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "UserDefinedHeatTransferCoefficient",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.math_utility import _1718
    from mastapy._private.math_utility.measured_data import _1749

    Self = TypeVar("Self", bound="UserDefinedHeatTransferCoefficient")
    CastSelf = TypeVar(
        "CastSelf",
        bound="UserDefinedHeatTransferCoefficient._Cast_UserDefinedHeatTransferCoefficient",
    )


__docformat__ = "restructuredtext en"
__all__ = ("UserDefinedHeatTransferCoefficient",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_UserDefinedHeatTransferCoefficient:
    """Special nested class for casting UserDefinedHeatTransferCoefficient to subclasses."""

    __parent__: "UserDefinedHeatTransferCoefficient"

    @property
    def user_defined_heat_transfer_coefficient(
        self: "CastSelf",
    ) -> "UserDefinedHeatTransferCoefficient":
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
class UserDefinedHeatTransferCoefficient(_0.APIBase):
    """UserDefinedHeatTransferCoefficient

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _USER_DEFINED_HEAT_TRANSFER_COEFFICIENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def extrapolation_options(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions":
        """EnumWithSelectedValue[mastapy.math_utility.ExtrapolationOptions]"""
        temp = pythonnet_property_get(self.wrapped, "ExtrapolationOptions")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @extrapolation_options.setter
    @exception_bridge
    @enforce_parameter_types
    def extrapolation_options(
        self: "Self", value: "_1694.ExtrapolationOptions"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ExtrapolationOptions", value)

    @property
    @exception_bridge
    def heat_transfer_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HeatTransferCoefficient")

        if temp is None:
            return 0.0

        return temp

    @heat_transfer_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def heat_transfer_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HeatTransferCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def heat_transfer_coefficient_specification_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_PropertySpecificationMethod":
        """EnumWithSelectedValue[mastapy.utility.enums.PropertySpecificationMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "HeatTransferCoefficientSpecificationMethod"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_PropertySpecificationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @heat_transfer_coefficient_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def heat_transfer_coefficient_specification_method(
        self: "Self", value: "_2017.PropertySpecificationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PropertySpecificationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "HeatTransferCoefficientSpecificationMethod", value
        )

    @property
    @exception_bridge
    def heat_transfer_coefficient_vs_volumetric_flow_rate(
        self: "Self",
    ) -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(
            self.wrapped, "HeatTransferCoefficientVsVolumetricFlowRate"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @heat_transfer_coefficient_vs_volumetric_flow_rate.setter
    @exception_bridge
    @enforce_parameter_types
    def heat_transfer_coefficient_vs_volumetric_flow_rate(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "HeatTransferCoefficientVsVolumetricFlowRate", value.wrapped
        )

    @property
    @exception_bridge
    def heat_transfer_coefficient_vs_volumetric_flow_rate_and_rotational_speed(
        self: "Self",
    ) -> "_1749.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(
            self.wrapped,
            "HeatTransferCoefficientVsVolumetricFlowRateAndRotationalSpeed",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @heat_transfer_coefficient_vs_volumetric_flow_rate_and_rotational_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def heat_transfer_coefficient_vs_volumetric_flow_rate_and_rotational_speed(
        self: "Self", value: "_1749.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "HeatTransferCoefficientVsVolumetricFlowRateAndRotationalSpeed",
            value.wrapped,
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
    def cast_to(self: "Self") -> "_Cast_UserDefinedHeatTransferCoefficient":
        """Cast to another type.

        Returns:
            _Cast_UserDefinedHeatTransferCoefficient
        """
        return _Cast_UserDefinedHeatTransferCoefficient(self)
