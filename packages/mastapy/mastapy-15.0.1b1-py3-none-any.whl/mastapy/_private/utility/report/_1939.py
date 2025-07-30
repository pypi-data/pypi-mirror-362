"""BlankRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1973

_BLANK_ROW = python_net_import("SMT.MastaAPI.Utility.Report", "BlankRow")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1968

    Self = TypeVar("Self", bound="BlankRow")
    CastSelf = TypeVar("CastSelf", bound="BlankRow._Cast_BlankRow")


__docformat__ = "restructuredtext en"
__all__ = ("BlankRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BlankRow:
    """Special nested class for casting BlankRow to subclasses."""

    __parent__: "BlankRow"

    @property
    def custom_row(self: "CastSelf") -> "_1973.CustomRow":
        return self.__parent__._cast(_1973.CustomRow)

    @property
    def custom_report_property_item(
        self: "CastSelf",
    ) -> "_1968.CustomReportPropertyItem":
        from mastapy._private.utility.report import _1968

        return self.__parent__._cast(_1968.CustomReportPropertyItem)

    @property
    def blank_row(self: "CastSelf") -> "BlankRow":
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
class BlankRow(_1973.CustomRow):
    """BlankRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BLANK_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BlankRow":
        """Cast to another type.

        Returns:
            _Cast_BlankRow
        """
        return _Cast_BlankRow(self)
