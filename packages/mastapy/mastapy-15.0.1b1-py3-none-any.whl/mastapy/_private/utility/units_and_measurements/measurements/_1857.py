"""LengthLong"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.units_and_measurements import _1797

_LENGTH_LONG = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements", "LengthLong"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LengthLong")
    CastSelf = TypeVar("CastSelf", bound="LengthLong._Cast_LengthLong")


__docformat__ = "restructuredtext en"
__all__ = ("LengthLong",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LengthLong:
    """Special nested class for casting LengthLong to subclasses."""

    __parent__: "LengthLong"

    @property
    def measurement_base(self: "CastSelf") -> "_1797.MeasurementBase":
        return self.__parent__._cast(_1797.MeasurementBase)

    @property
    def length_long(self: "CastSelf") -> "LengthLong":
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
class LengthLong(_1797.MeasurementBase):
    """LengthLong

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LENGTH_LONG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LengthLong":
        """Cast to another type.

        Returns:
            _Cast_LengthLong
        """
        return _Cast_LengthLong(self)
