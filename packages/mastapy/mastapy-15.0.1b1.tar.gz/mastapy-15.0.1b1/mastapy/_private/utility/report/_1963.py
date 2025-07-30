"""CustomReportKey"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.databases import _2025

_CUSTOM_REPORT_KEY = python_net_import("SMT.MastaAPI.Utility.Report", "CustomReportKey")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CustomReportKey")
    CastSelf = TypeVar("CastSelf", bound="CustomReportKey._Cast_CustomReportKey")


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportKey",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportKey:
    """Special nested class for casting CustomReportKey to subclasses."""

    __parent__: "CustomReportKey"

    @property
    def database_key(self: "CastSelf") -> "_2025.DatabaseKey":
        return self.__parent__._cast(_2025.DatabaseKey)

    @property
    def custom_report_key(self: "CastSelf") -> "CustomReportKey":
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
class CustomReportKey(_2025.DatabaseKey):
    """CustomReportKey

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_KEY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportKey":
        """Cast to another type.

        Returns:
            _Cast_CustomReportKey
        """
        return _Cast_CustomReportKey(self)
