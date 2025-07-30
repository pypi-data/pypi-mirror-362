"""Customer102DataSheetChangeLog"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)

_CUSTOMER_102_DATA_SHEET_CHANGE_LOG = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "Customer102DataSheetChangeLog"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1111

    Self = TypeVar("Self", bound="Customer102DataSheetChangeLog")
    CastSelf = TypeVar(
        "CastSelf",
        bound="Customer102DataSheetChangeLog._Cast_Customer102DataSheetChangeLog",
    )


__docformat__ = "restructuredtext en"
__all__ = ("Customer102DataSheetChangeLog",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Customer102DataSheetChangeLog:
    """Special nested class for casting Customer102DataSheetChangeLog to subclasses."""

    __parent__: "Customer102DataSheetChangeLog"

    @property
    def customer_102_data_sheet_change_log(
        self: "CastSelf",
    ) -> "Customer102DataSheetChangeLog":
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
class Customer102DataSheetChangeLog(_0.APIBase):
    """Customer102DataSheetChangeLog

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOMER_102_DATA_SHEET_CHANGE_LOG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def customer_102_data_sheet_change_log_items(
        self: "Self",
    ) -> "List[_1111.Customer102DataSheetChangeLogItem]":
        """List[mastapy.gears.gear_designs.cylindrical.Customer102DataSheetChangeLogItem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "Customer102DataSheetChangeLogItems"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def add_entry_to_change_log(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddEntryToChangeLog")

    @property
    def cast_to(self: "Self") -> "_Cast_Customer102DataSheetChangeLog":
        """Cast to another type.

        Returns:
            _Cast_Customer102DataSheetChangeLog
        """
        return _Cast_Customer102DataSheetChangeLog(self)
