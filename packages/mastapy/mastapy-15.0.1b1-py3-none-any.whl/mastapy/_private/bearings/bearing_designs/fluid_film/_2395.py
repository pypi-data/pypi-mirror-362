"""CircumferentialFeedJournalBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CIRCUMFERENTIAL_FEED_JOURNAL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm",
    "CircumferentialFeedJournalBearing",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CircumferentialFeedJournalBearing")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CircumferentialFeedJournalBearing._Cast_CircumferentialFeedJournalBearing",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CircumferentialFeedJournalBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CircumferentialFeedJournalBearing:
    """Special nested class for casting CircumferentialFeedJournalBearing to subclasses."""

    __parent__: "CircumferentialFeedJournalBearing"

    @property
    def circumferential_feed_journal_bearing(
        self: "CastSelf",
    ) -> "CircumferentialFeedJournalBearing":
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
class CircumferentialFeedJournalBearing(_0.APIBase):
    """CircumferentialFeedJournalBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CIRCUMFERENTIAL_FEED_JOURNAL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def groove_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GrooveWidth")

        if temp is None:
            return 0.0

        return temp

    @groove_width.setter
    @exception_bridge
    @enforce_parameter_types
    def groove_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "GrooveWidth", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CircumferentialFeedJournalBearing":
        """Cast to another type.

        Returns:
            _Cast_CircumferentialFeedJournalBearing
        """
        return _Cast_CircumferentialFeedJournalBearing(self)
