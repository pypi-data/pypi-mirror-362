"""ParetoOptimisationStrategyChartInformation"""

from __future__ import annotations

from enum import Enum
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

_PARETO_OPTIMISATION_STRATEGY_CHART_INFORMATION = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation",
    "ParetoOptimisationStrategyChartInformation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.math_utility.optimisation import _1734

    Self = TypeVar("Self", bound="ParetoOptimisationStrategyChartInformation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ParetoOptimisationStrategyChartInformation._Cast_ParetoOptimisationStrategyChartInformation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParetoOptimisationStrategyChartInformation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParetoOptimisationStrategyChartInformation:
    """Special nested class for casting ParetoOptimisationStrategyChartInformation to subclasses."""

    __parent__: "ParetoOptimisationStrategyChartInformation"

    @property
    def pareto_optimisation_strategy_chart_information(
        self: "CastSelf",
    ) -> "ParetoOptimisationStrategyChartInformation":
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
class ParetoOptimisationStrategyChartInformation(_0.APIBase):
    """ParetoOptimisationStrategyChartInformation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARETO_OPTIMISATION_STRATEGY_CHART_INFORMATION

    class ScatterOrBarChart(Enum):
        """ScatterOrBarChart is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _PARETO_OPTIMISATION_STRATEGY_CHART_INFORMATION.ScatterOrBarChart

        SCATTER_CHART = 0
        BAR_AND_LINE_CHART = 1

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    ScatterOrBarChart.__setattr__ = __enum_setattr
    ScatterOrBarChart.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def chart_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "ChartName")

        if temp is None:
            return ""

        return temp

    @chart_name.setter
    @exception_bridge
    @enforce_parameter_types
    def chart_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "ChartName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def select_chart_type(
        self: "Self",
    ) -> "ParetoOptimisationStrategyChartInformation.ScatterOrBarChart":
        """mastapy.math_utility.optimisation.ParetoOptimisationStrategyChartInformation.ScatterOrBarChart"""
        temp = pythonnet_property_get(self.wrapped, "SelectChartType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.MathUtility.Optimisation.ParetoOptimisationStrategyChartInformation+ScatterOrBarChart",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility.optimisation.ParetoOptimisationStrategyChartInformation.ParetoOptimisationStrategyChartInformation",
            "ScatterOrBarChart",
        )(value)

    @select_chart_type.setter
    @exception_bridge
    @enforce_parameter_types
    def select_chart_type(
        self: "Self",
        value: "ParetoOptimisationStrategyChartInformation.ScatterOrBarChart",
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.MathUtility.Optimisation.ParetoOptimisationStrategyChartInformation+ScatterOrBarChart",
        )
        pythonnet_property_set(self.wrapped, "SelectChartType", value)

    @property
    @exception_bridge
    def bars(self: "Self") -> "List[_1734.ParetoOptimisationStrategyBars]":
        """List[mastapy.math_utility.optimisation.ParetoOptimisationStrategyBars]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bars")

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
    def add_bar(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddBar")

    @exception_bridge
    def remove_chart(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveChart")

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
    def cast_to(self: "Self") -> "_Cast_ParetoOptimisationStrategyChartInformation":
        """Cast to another type.

        Returns:
            _Cast_ParetoOptimisationStrategyChartInformation
        """
        return _Cast_ParetoOptimisationStrategyChartInformation(self)
