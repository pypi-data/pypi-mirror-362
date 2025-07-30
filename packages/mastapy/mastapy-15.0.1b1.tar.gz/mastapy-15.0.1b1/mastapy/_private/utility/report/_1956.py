"""CustomReportHorizontalLine"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1958

_CUSTOM_REPORT_HORIZONTAL_LINE = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportHorizontalLine"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CustomReportHorizontalLine")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportHorizontalLine._Cast_CustomReportHorizontalLine"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportHorizontalLine",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportHorizontalLine:
    """Special nested class for casting CustomReportHorizontalLine to subclasses."""

    __parent__: "CustomReportHorizontalLine"

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def custom_report_horizontal_line(self: "CastSelf") -> "CustomReportHorizontalLine":
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
class CustomReportHorizontalLine(_1958.CustomReportItem):
    """CustomReportHorizontalLine

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_HORIZONTAL_LINE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportHorizontalLine":
        """Cast to another type.

        Returns:
            _Cast_CustomReportHorizontalLine
        """
        return _Cast_CustomReportHorizontalLine(self)
