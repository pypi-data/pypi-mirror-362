"""Pressure"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.units_and_measurements.measurements import _1908

_PRESSURE = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements", "Pressure"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.units_and_measurements import _1797

    Self = TypeVar("Self", bound="Pressure")
    CastSelf = TypeVar("CastSelf", bound="Pressure._Cast_Pressure")


__docformat__ = "restructuredtext en"
__all__ = ("Pressure",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Pressure:
    """Special nested class for casting Pressure to subclasses."""

    __parent__: "Pressure"

    @property
    def stress(self: "CastSelf") -> "_1908.Stress":
        return self.__parent__._cast(_1908.Stress)

    @property
    def measurement_base(self: "CastSelf") -> "_1797.MeasurementBase":
        from mastapy._private.utility.units_and_measurements import _1797

        return self.__parent__._cast(_1797.MeasurementBase)

    @property
    def pressure(self: "CastSelf") -> "Pressure":
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
class Pressure(_1908.Stress):
    """Pressure

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PRESSURE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_Pressure":
        """Cast to another type.

        Returns:
            _Cast_Pressure
        """
        return _Cast_Pressure(self)
