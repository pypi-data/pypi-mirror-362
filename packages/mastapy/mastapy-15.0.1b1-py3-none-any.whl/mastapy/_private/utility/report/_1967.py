"""CustomReportNamedItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1966

_CUSTOM_REPORT_NAMED_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportNamedItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1958

    Self = TypeVar("Self", bound="CustomReportNamedItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportNamedItem._Cast_CustomReportNamedItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportNamedItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportNamedItem:
    """Special nested class for casting CustomReportNamedItem to subclasses."""

    __parent__: "CustomReportNamedItem"

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
    def custom_report_named_item(self: "CastSelf") -> "CustomReportNamedItem":
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
class CustomReportNamedItem(_1966.CustomReportNameableItem):
    """CustomReportNamedItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_NAMED_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportNamedItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportNamedItem
        """
        return _Cast_CustomReportNamedItem(self)
