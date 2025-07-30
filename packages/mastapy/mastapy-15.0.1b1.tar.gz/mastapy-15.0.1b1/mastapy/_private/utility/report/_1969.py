"""CustomReportStatusItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1955

_CUSTOM_REPORT_STATUS_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportStatusItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1958, _1966

    Self = TypeVar("Self", bound="CustomReportStatusItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportStatusItem._Cast_CustomReportStatusItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportStatusItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportStatusItem:
    """Special nested class for casting CustomReportStatusItem to subclasses."""

    __parent__: "CustomReportStatusItem"

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1955.CustomReportDefinitionItem":
        return self.__parent__._cast(_1955.CustomReportDefinitionItem)

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
    def custom_report_status_item(self: "CastSelf") -> "CustomReportStatusItem":
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
class CustomReportStatusItem(_1955.CustomReportDefinitionItem):
    """CustomReportStatusItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_STATUS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportStatusItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportStatusItem
        """
        return _Cast_CustomReportStatusItem(self)
