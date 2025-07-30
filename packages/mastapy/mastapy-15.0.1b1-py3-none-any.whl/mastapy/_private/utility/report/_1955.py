"""CustomReportDefinitionItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1966

_CUSTOM_REPORT_DEFINITION_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportDefinitionItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2153
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4653,
    )
    from mastapy._private.utility.report import (
        _1937,
        _1945,
        _1946,
        _1947,
        _1948,
        _1957,
        _1958,
        _1969,
        _1972,
        _1974,
    )

    Self = TypeVar("Self", bound="CustomReportDefinitionItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportDefinitionItem._Cast_CustomReportDefinitionItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportDefinitionItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportDefinitionItem:
    """Special nested class for casting CustomReportDefinitionItem to subclasses."""

    __parent__: "CustomReportDefinitionItem"

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1966.CustomReportNameableItem":
        return self.__parent__._cast(_1966.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def ad_hoc_custom_table(self: "CastSelf") -> "_1937.AdHocCustomTable":
        from mastapy._private.utility.report import _1937

        return self.__parent__._cast(_1937.AdHocCustomTable)

    @property
    def custom_chart(self: "CastSelf") -> "_1945.CustomChart":
        from mastapy._private.utility.report import _1945

        return self.__parent__._cast(_1945.CustomChart)

    @property
    def custom_drawing(self: "CastSelf") -> "_1946.CustomDrawing":
        from mastapy._private.utility.report import _1946

        return self.__parent__._cast(_1946.CustomDrawing)

    @property
    def custom_graphic(self: "CastSelf") -> "_1947.CustomGraphic":
        from mastapy._private.utility.report import _1947

        return self.__parent__._cast(_1947.CustomGraphic)

    @property
    def custom_image(self: "CastSelf") -> "_1948.CustomImage":
        from mastapy._private.utility.report import _1948

        return self.__parent__._cast(_1948.CustomImage)

    @property
    def custom_report_html_item(self: "CastSelf") -> "_1957.CustomReportHtmlItem":
        from mastapy._private.utility.report import _1957

        return self.__parent__._cast(_1957.CustomReportHtmlItem)

    @property
    def custom_report_status_item(self: "CastSelf") -> "_1969.CustomReportStatusItem":
        from mastapy._private.utility.report import _1969

        return self.__parent__._cast(_1969.CustomReportStatusItem)

    @property
    def custom_report_text(self: "CastSelf") -> "_1972.CustomReportText":
        from mastapy._private.utility.report import _1972

        return self.__parent__._cast(_1972.CustomReportText)

    @property
    def custom_sub_report(self: "CastSelf") -> "_1974.CustomSubReport":
        from mastapy._private.utility.report import _1974

        return self.__parent__._cast(_1974.CustomSubReport)

    @property
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2153.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2153

        return self.__parent__._cast(_2153.LoadedBearingChartReporter)

    @property
    def parametric_study_histogram(
        self: "CastSelf",
    ) -> "_4653.ParametricStudyHistogram":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4653,
        )

        return self.__parent__._cast(_4653.ParametricStudyHistogram)

    @property
    def custom_report_definition_item(self: "CastSelf") -> "CustomReportDefinitionItem":
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
class CustomReportDefinitionItem(_1966.CustomReportNameableItem):
    """CustomReportDefinitionItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_DEFINITION_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportDefinitionItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportDefinitionItem
        """
        return _Cast_CustomReportDefinitionItem(self)
