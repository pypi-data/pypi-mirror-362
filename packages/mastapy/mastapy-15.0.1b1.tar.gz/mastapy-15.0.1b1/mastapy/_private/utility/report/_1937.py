"""AdHocCustomTable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1955

_AD_HOC_CUSTOM_TABLE = python_net_import(
    "SMT.MastaAPI.Utility.Report", "AdHocCustomTable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1958, _1966

    Self = TypeVar("Self", bound="AdHocCustomTable")
    CastSelf = TypeVar("CastSelf", bound="AdHocCustomTable._Cast_AdHocCustomTable")


__docformat__ = "restructuredtext en"
__all__ = ("AdHocCustomTable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AdHocCustomTable:
    """Special nested class for casting AdHocCustomTable to subclasses."""

    __parent__: "AdHocCustomTable"

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
    def ad_hoc_custom_table(self: "CastSelf") -> "AdHocCustomTable":
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
class AdHocCustomTable(_1955.CustomReportDefinitionItem):
    """AdHocCustomTable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AD_HOC_CUSTOM_TABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AdHocCustomTable":
        """Cast to another type.

        Returns:
            _Cast_AdHocCustomTable
        """
        return _Cast_AdHocCustomTable(self)
