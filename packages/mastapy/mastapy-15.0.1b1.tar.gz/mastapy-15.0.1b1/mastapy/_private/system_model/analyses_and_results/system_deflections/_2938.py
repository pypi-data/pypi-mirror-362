"""BearingDynamicResultsUIWrapper"""

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

_BEARING_DYNAMIC_RESULTS_UI_WRAPPER = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "BearingDynamicResultsUIWrapper",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings.bearing_results.rolling.dysla import _2324
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2935,
        _2936,
        _2937,
        _2939,
    )

    Self = TypeVar("Self", bound="BearingDynamicResultsUIWrapper")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BearingDynamicResultsUIWrapper._Cast_BearingDynamicResultsUIWrapper",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingDynamicResultsUIWrapper",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingDynamicResultsUIWrapper:
    """Special nested class for casting BearingDynamicResultsUIWrapper to subclasses."""

    __parent__: "BearingDynamicResultsUIWrapper"

    @property
    def bearing_dynamic_results_ui_wrapper(
        self: "CastSelf",
    ) -> "BearingDynamicResultsUIWrapper":
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
class BearingDynamicResultsUIWrapper(_0.APIBase):
    """BearingDynamicResultsUIWrapper

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_DYNAMIC_RESULTS_UI_WRAPPER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_revolutions_to_plot(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumRevolutionsToPlot")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_revolutions_to_plot.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_revolutions_to_plot(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumRevolutionsToPlot", value)

    @property
    @exception_bridge
    def maximum_time_to_plot(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumTimeToPlot")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_time_to_plot.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_time_to_plot(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumTimeToPlot", value)

    @property
    @exception_bridge
    def minimum_revolutions_to_plot(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumRevolutionsToPlot")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_revolutions_to_plot.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_revolutions_to_plot(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumRevolutionsToPlot", value)

    @property
    @exception_bridge
    def minimum_time_to_plot(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumTimeToPlot")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_time_to_plot.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_time_to_plot(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumTimeToPlot", value)

    @property
    @exception_bridge
    def plot_against_number_of_revolutions(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "PlotAgainstNumberOfRevolutions")

        if temp is None:
            return False

        return temp

    @plot_against_number_of_revolutions.setter
    @exception_bridge
    @enforce_parameter_types
    def plot_against_number_of_revolutions(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PlotAgainstNumberOfRevolutions",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def revolutions_type(self: "Self") -> "_2324.RevolutionsType":
        """mastapy.bearings.bearing_results.rolling.dysla.RevolutionsType"""
        temp = pythonnet_property_get(self.wrapped, "RevolutionsType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingResults.Rolling.Dysla.RevolutionsType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results.rolling.dysla._2324",
            "RevolutionsType",
        )(value)

    @revolutions_type.setter
    @exception_bridge
    @enforce_parameter_types
    def revolutions_type(self: "Self", value: "_2324.RevolutionsType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingResults.Rolling.Dysla.RevolutionsType"
        )
        pythonnet_property_set(self.wrapped, "RevolutionsType", value)

    @property
    @exception_bridge
    def bearing_system_deflection(self: "Self") -> "_2939.BearingSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.BearingSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingSystemDeflection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bearing_results(
        self: "Self",
    ) -> "List[_2937.BearingDynamicResultsPropertyWrapper]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BearingDynamicResultsPropertyWrapper]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cage_results(
        self: "Self",
    ) -> "List[_2937.BearingDynamicResultsPropertyWrapper]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BearingDynamicResultsPropertyWrapper]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CageResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def element_results(
        self: "Self",
    ) -> "List[_2935.BearingDynamicElementPropertyWrapper]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BearingDynamicElementPropertyWrapper]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def post_analysis_results(
        self: "Self",
    ) -> "List[_2936.BearingDynamicPostAnalysisResultWrapper]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BearingDynamicPostAnalysisResultWrapper]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PostAnalysisResults")

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
    def clear_all_plots(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearAllPlots")

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
    def cast_to(self: "Self") -> "_Cast_BearingDynamicResultsUIWrapper":
        """Cast to another type.

        Returns:
            _Cast_BearingDynamicResultsUIWrapper
        """
        return _Cast_BearingDynamicResultsUIWrapper(self)
