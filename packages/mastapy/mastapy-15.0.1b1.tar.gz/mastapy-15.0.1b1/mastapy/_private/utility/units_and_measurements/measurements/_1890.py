"""PowerSmallPerUnitTime"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.units_and_measurements import _1797

_POWER_SMALL_PER_UNIT_TIME = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements", "PowerSmallPerUnitTime"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PowerSmallPerUnitTime")
    CastSelf = TypeVar(
        "CastSelf", bound="PowerSmallPerUnitTime._Cast_PowerSmallPerUnitTime"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PowerSmallPerUnitTime",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PowerSmallPerUnitTime:
    """Special nested class for casting PowerSmallPerUnitTime to subclasses."""

    __parent__: "PowerSmallPerUnitTime"

    @property
    def measurement_base(self: "CastSelf") -> "_1797.MeasurementBase":
        return self.__parent__._cast(_1797.MeasurementBase)

    @property
    def power_small_per_unit_time(self: "CastSelf") -> "PowerSmallPerUnitTime":
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
class PowerSmallPerUnitTime(_1797.MeasurementBase):
    """PowerSmallPerUnitTime

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POWER_SMALL_PER_UNIT_TIME

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PowerSmallPerUnitTime":
        """Cast to another type.

        Returns:
            _Cast_PowerSmallPerUnitTime
        """
        return _Cast_PowerSmallPerUnitTime(self)
