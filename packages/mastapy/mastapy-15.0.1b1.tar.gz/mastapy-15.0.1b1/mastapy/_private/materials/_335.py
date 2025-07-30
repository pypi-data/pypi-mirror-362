"""BHCurveSpecification"""

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

_BH_CURVE_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Materials", "BHCurveSpecification"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.materials import _334
    from mastapy._private.math_utility import _1718
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="BHCurveSpecification")
    CastSelf = TypeVar(
        "CastSelf", bound="BHCurveSpecification._Cast_BHCurveSpecification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BHCurveSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BHCurveSpecification:
    """Special nested class for casting BHCurveSpecification to subclasses."""

    __parent__: "BHCurveSpecification"

    @property
    def bh_curve_specification(self: "CastSelf") -> "BHCurveSpecification":
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
class BHCurveSpecification(_0.APIBase):
    """BHCurveSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BH_CURVE_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bh_curve(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "BHCurve")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @bh_curve.setter
    @exception_bridge
    @enforce_parameter_types
    def bh_curve(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "BHCurve", value.wrapped)

    @property
    @exception_bridge
    def bh_curve_plot(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BHCurvePlot")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bh_curve_extrapolation_method(
        self: "Self",
    ) -> "_334.BHCurveExtrapolationMethod":
        """mastapy.materials.BHCurveExtrapolationMethod"""
        temp = pythonnet_property_get(self.wrapped, "BHCurveExtrapolationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.BHCurveExtrapolationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._334", "BHCurveExtrapolationMethod"
        )(value)

    @bh_curve_extrapolation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def bh_curve_extrapolation_method(
        self: "Self", value: "_334.BHCurveExtrapolationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.BHCurveExtrapolationMethod"
        )
        pythonnet_property_set(self.wrapped, "BHCurveExtrapolationMethod", value)

    @property
    @exception_bridge
    def maximum_h_for_bh_curve_extrapolation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumHForBHCurveExtrapolation")

        if temp is None:
            return 0.0

        return temp

    @maximum_h_for_bh_curve_extrapolation.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_h_for_bh_curve_extrapolation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumHForBHCurveExtrapolation",
            float(value) if value is not None else 0.0,
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
    def number_of_points_for_bh_curve_extrapolation(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsForBHCurveExtrapolation"
        )

        if temp is None:
            return 0

        return temp

    @number_of_points_for_bh_curve_extrapolation.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_for_bh_curve_extrapolation(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPointsForBHCurveExtrapolation",
            int(value) if value is not None else 0,
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
    def cast_to(self: "Self") -> "_Cast_BHCurveSpecification":
        """Cast to another type.

        Returns:
            _Cast_BHCurveSpecification
        """
        return _Cast_BHCurveSpecification(self)
