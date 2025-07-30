"""DegreesMinutesSeconds"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.units_and_measurements import _1802

_DEGREES_MINUTES_SECONDS = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements", "DegreesMinutesSeconds"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DegreesMinutesSeconds")
    CastSelf = TypeVar(
        "CastSelf", bound="DegreesMinutesSeconds._Cast_DegreesMinutesSeconds"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DegreesMinutesSeconds",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DegreesMinutesSeconds:
    """Special nested class for casting DegreesMinutesSeconds to subclasses."""

    __parent__: "DegreesMinutesSeconds"

    @property
    def unit(self: "CastSelf") -> "_1802.Unit":
        return self.__parent__._cast(_1802.Unit)

    @property
    def degrees_minutes_seconds(self: "CastSelf") -> "DegreesMinutesSeconds":
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
class DegreesMinutesSeconds(_1802.Unit):
    """DegreesMinutesSeconds

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DEGREES_MINUTES_SECONDS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DegreesMinutesSeconds":
        """Cast to another type.

        Returns:
            _Cast_DegreesMinutesSeconds
        """
        return _Cast_DegreesMinutesSeconds(self)
