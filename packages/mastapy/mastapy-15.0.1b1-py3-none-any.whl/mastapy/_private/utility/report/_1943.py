"""ChartDefinition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CHART_DEFINITION = python_net_import("SMT.MastaAPI.Utility.Report", "ChartDefinition")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.utility.report import _1981
    from mastapy._private.utility_gui.charts import (
        _2055,
        _2059,
        _2060,
        _2062,
        _2063,
        _2065,
        _2068,
        _2069,
        _2070,
    )

    Self = TypeVar("Self", bound="ChartDefinition")
    CastSelf = TypeVar("CastSelf", bound="ChartDefinition._Cast_ChartDefinition")


__docformat__ = "restructuredtext en"
__all__ = ("ChartDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ChartDefinition:
    """Special nested class for casting ChartDefinition to subclasses."""

    __parent__: "ChartDefinition"

    @property
    def simple_chart_definition(self: "CastSelf") -> "_1981.SimpleChartDefinition":
        from mastapy._private.utility.report import _1981

        return self.__parent__._cast(_1981.SimpleChartDefinition)

    @property
    def bubble_chart_definition(self: "CastSelf") -> "_2055.BubbleChartDefinition":
        from mastapy._private.utility_gui.charts import _2055

        return self.__parent__._cast(_2055.BubbleChartDefinition)

    @property
    def legacy_chart_math_chart_definition(
        self: "CastSelf",
    ) -> "_2059.LegacyChartMathChartDefinition":
        from mastapy._private.utility_gui.charts import _2059

        return self.__parent__._cast(_2059.LegacyChartMathChartDefinition)

    @property
    def matrix_visualisation_definition(
        self: "CastSelf",
    ) -> "_2060.MatrixVisualisationDefinition":
        from mastapy._private.utility_gui.charts import _2060

        return self.__parent__._cast(_2060.MatrixVisualisationDefinition)

    @property
    def nd_chart_definition(self: "CastSelf") -> "_2062.NDChartDefinition":
        from mastapy._private.utility_gui.charts import _2062

        return self.__parent__._cast(_2062.NDChartDefinition)

    @property
    def parallel_coordinates_chart_definition(
        self: "CastSelf",
    ) -> "_2063.ParallelCoordinatesChartDefinition":
        from mastapy._private.utility_gui.charts import _2063

        return self.__parent__._cast(_2063.ParallelCoordinatesChartDefinition)

    @property
    def scatter_chart_definition(self: "CastSelf") -> "_2065.ScatterChartDefinition":
        from mastapy._private.utility_gui.charts import _2065

        return self.__parent__._cast(_2065.ScatterChartDefinition)

    @property
    def three_d_chart_definition(self: "CastSelf") -> "_2068.ThreeDChartDefinition":
        from mastapy._private.utility_gui.charts import _2068

        return self.__parent__._cast(_2068.ThreeDChartDefinition)

    @property
    def three_d_vector_chart_definition(
        self: "CastSelf",
    ) -> "_2069.ThreeDVectorChartDefinition":
        from mastapy._private.utility_gui.charts import _2069

        return self.__parent__._cast(_2069.ThreeDVectorChartDefinition)

    @property
    def two_d_chart_definition(self: "CastSelf") -> "_2070.TwoDChartDefinition":
        from mastapy._private.utility_gui.charts import _2070

        return self.__parent__._cast(_2070.TwoDChartDefinition)

    @property
    def chart_definition(self: "CastSelf") -> "ChartDefinition":
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
class ChartDefinition(_0.APIBase):
    """ChartDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CHART_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def to_bitmap(self: "Self") -> "Image":
        """Image"""
        return conversion.pn_to_mp_smt_bitmap(
            pythonnet_method_call(self.wrapped, "ToBitmap")
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
    def cast_to(self: "Self") -> "_Cast_ChartDefinition":
        """Cast to another type.

        Returns:
            _Cast_ChartDefinition
        """
        return _Cast_ChartDefinition(self)
