"""PressureSmall"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.units_and_measurements.measurements import _1908

_PRESSURE_SMALL = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements", "PressureSmall"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.units_and_measurements import _1797

    Self = TypeVar("Self", bound="PressureSmall")
    CastSelf = TypeVar("CastSelf", bound="PressureSmall._Cast_PressureSmall")


__docformat__ = "restructuredtext en"
__all__ = ("PressureSmall",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PressureSmall:
    """Special nested class for casting PressureSmall to subclasses."""

    __parent__: "PressureSmall"

    @property
    def stress(self: "CastSelf") -> "_1908.Stress":
        return self.__parent__._cast(_1908.Stress)

    @property
    def measurement_base(self: "CastSelf") -> "_1797.MeasurementBase":
        from mastapy._private.utility.units_and_measurements import _1797

        return self.__parent__._cast(_1797.MeasurementBase)

    @property
    def pressure_small(self: "CastSelf") -> "PressureSmall":
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
class PressureSmall(_1908.Stress):
    """PressureSmall

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PRESSURE_SMALL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PressureSmall":
        """Cast to another type.

        Returns:
            _Cast_PressureSmall
        """
        return _Cast_PressureSmall(self)
