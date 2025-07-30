"""LengthVeryShortPerLengthShort"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.units_and_measurements import _1797

_LENGTH_VERY_SHORT_PER_LENGTH_SHORT = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements",
    "LengthVeryShortPerLengthShort",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LengthVeryShortPerLengthShort")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LengthVeryShortPerLengthShort._Cast_LengthVeryShortPerLengthShort",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LengthVeryShortPerLengthShort",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LengthVeryShortPerLengthShort:
    """Special nested class for casting LengthVeryShortPerLengthShort to subclasses."""

    __parent__: "LengthVeryShortPerLengthShort"

    @property
    def measurement_base(self: "CastSelf") -> "_1797.MeasurementBase":
        return self.__parent__._cast(_1797.MeasurementBase)

    @property
    def length_very_short_per_length_short(
        self: "CastSelf",
    ) -> "LengthVeryShortPerLengthShort":
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
class LengthVeryShortPerLengthShort(_1797.MeasurementBase):
    """LengthVeryShortPerLengthShort

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LENGTH_VERY_SHORT_PER_LENGTH_SHORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LengthVeryShortPerLengthShort":
        """Cast to another type.

        Returns:
            _Cast_LengthVeryShortPerLengthShort
        """
        return _Cast_LengthVeryShortPerLengthShort(self)
