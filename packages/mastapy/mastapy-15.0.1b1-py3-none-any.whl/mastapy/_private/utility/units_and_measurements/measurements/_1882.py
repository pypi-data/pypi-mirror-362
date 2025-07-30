"""Percentage"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.units_and_measurements.measurements import _1839

_PERCENTAGE = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements", "Percentage"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.units_and_measurements import _1797

    Self = TypeVar("Self", bound="Percentage")
    CastSelf = TypeVar("CastSelf", bound="Percentage._Cast_Percentage")


__docformat__ = "restructuredtext en"
__all__ = ("Percentage",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Percentage:
    """Special nested class for casting Percentage to subclasses."""

    __parent__: "Percentage"

    @property
    def fraction_measurement_base(self: "CastSelf") -> "_1839.FractionMeasurementBase":
        return self.__parent__._cast(_1839.FractionMeasurementBase)

    @property
    def measurement_base(self: "CastSelf") -> "_1797.MeasurementBase":
        from mastapy._private.utility.units_and_measurements import _1797

        return self.__parent__._cast(_1797.MeasurementBase)

    @property
    def percentage(self: "CastSelf") -> "Percentage":
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
class Percentage(_1839.FractionMeasurementBase):
    """Percentage

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PERCENTAGE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_Percentage":
        """Cast to another type.

        Returns:
            _Cast_Percentage
        """
        return _Cast_Percentage(self)
