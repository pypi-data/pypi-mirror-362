"""CustomReportItemContainerCollectionItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1959

_CUSTOM_REPORT_ITEM_CONTAINER_COLLECTION_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportItemContainerCollectionItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1953, _1958, _1970

    Self = TypeVar("Self", bound="CustomReportItemContainerCollectionItem")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CustomReportItemContainerCollectionItem._Cast_CustomReportItemContainerCollectionItem",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportItemContainerCollectionItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportItemContainerCollectionItem:
    """Special nested class for casting CustomReportItemContainerCollectionItem to subclasses."""

    __parent__: "CustomReportItemContainerCollectionItem"

    @property
    def custom_report_item_container(
        self: "CastSelf",
    ) -> "_1959.CustomReportItemContainer":
        return self.__parent__._cast(_1959.CustomReportItemContainer)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def custom_report_column(self: "CastSelf") -> "_1953.CustomReportColumn":
        from mastapy._private.utility.report import _1953

        return self.__parent__._cast(_1953.CustomReportColumn)

    @property
    def custom_report_tab(self: "CastSelf") -> "_1970.CustomReportTab":
        from mastapy._private.utility.report import _1970

        return self.__parent__._cast(_1970.CustomReportTab)

    @property
    def custom_report_item_container_collection_item(
        self: "CastSelf",
    ) -> "CustomReportItemContainerCollectionItem":
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
class CustomReportItemContainerCollectionItem(_1959.CustomReportItemContainer):
    """CustomReportItemContainerCollectionItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_ITEM_CONTAINER_COLLECTION_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportItemContainerCollectionItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportItemContainerCollectionItem
        """
        return _Cast_CustomReportItemContainerCollectionItem(self)
