"""CustomReportItemContainerCollection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1961

_CUSTOM_REPORT_ITEM_CONTAINER_COLLECTION = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportItemContainerCollection"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.utility.report import _1954, _1958, _1962, _1971

    Self = TypeVar("Self", bound="CustomReportItemContainerCollection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CustomReportItemContainerCollection._Cast_CustomReportItemContainerCollection",
    )

T = TypeVar("T", bound="_1962.CustomReportItemContainerCollectionItem")

__docformat__ = "restructuredtext en"
__all__ = ("CustomReportItemContainerCollection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportItemContainerCollection:
    """Special nested class for casting CustomReportItemContainerCollection to subclasses."""

    __parent__: "CustomReportItemContainerCollection"

    @property
    def custom_report_item_container_collection_base(
        self: "CastSelf",
    ) -> "_1961.CustomReportItemContainerCollectionBase":
        return self.__parent__._cast(_1961.CustomReportItemContainerCollectionBase)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def custom_report_columns(self: "CastSelf") -> "_1954.CustomReportColumns":
        from mastapy._private.utility.report import _1954

        return self.__parent__._cast(_1954.CustomReportColumns)

    @property
    def custom_report_tabs(self: "CastSelf") -> "_1971.CustomReportTabs":
        from mastapy._private.utility.report import _1971

        return self.__parent__._cast(_1971.CustomReportTabs)

    @property
    def custom_report_item_container_collection(
        self: "CastSelf",
    ) -> "CustomReportItemContainerCollection":
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
class CustomReportItemContainerCollection(
    _1961.CustomReportItemContainerCollectionBase, Generic[T]
):
    """CustomReportItemContainerCollection

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_ITEM_CONTAINER_COLLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportItemContainerCollection":
        """Cast to another type.

        Returns:
            _Cast_CustomReportItemContainerCollection
        """
        return _Cast_CustomReportItemContainerCollection(self)
