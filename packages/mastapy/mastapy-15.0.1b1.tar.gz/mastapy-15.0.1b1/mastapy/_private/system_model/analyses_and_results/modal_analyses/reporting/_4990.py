"""CampbellDiagramReport"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1951

_CAMPBELL_DIAGRAM_REPORT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting",
    "CampbellDiagramReport",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1958, _1964, _1965, _1966

    Self = TypeVar("Self", bound="CampbellDiagramReport")
    CastSelf = TypeVar(
        "CastSelf", bound="CampbellDiagramReport._Cast_CampbellDiagramReport"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CampbellDiagramReport",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CampbellDiagramReport:
    """Special nested class for casting CampbellDiagramReport to subclasses."""

    __parent__: "CampbellDiagramReport"

    @property
    def custom_report_chart(self: "CastSelf") -> "_1951.CustomReportChart":
        return self.__parent__._cast(_1951.CustomReportChart)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1964.CustomReportMultiPropertyItem":
        pass

        from mastapy._private.utility.report import _1964

        return self.__parent__._cast(_1964.CustomReportMultiPropertyItem)

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1965.CustomReportMultiPropertyItemBase":
        from mastapy._private.utility.report import _1965

        return self.__parent__._cast(_1965.CustomReportMultiPropertyItemBase)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1966.CustomReportNameableItem":
        from mastapy._private.utility.report import _1966

        return self.__parent__._cast(_1966.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def campbell_diagram_report(self: "CastSelf") -> "CampbellDiagramReport":
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
class CampbellDiagramReport(_1951.CustomReportChart):
    """CampbellDiagramReport

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CAMPBELL_DIAGRAM_REPORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CampbellDiagramReport":
        """Cast to another type.

        Returns:
            _Cast_CampbellDiagramReport
        """
        return _Cast_CampbellDiagramReport(self)
