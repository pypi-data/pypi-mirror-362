"""CarbonEmissionFactor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.units_and_measurements import _1797

_CARBON_EMISSION_FACTOR = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements", "CarbonEmissionFactor"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CarbonEmissionFactor")
    CastSelf = TypeVar(
        "CastSelf", bound="CarbonEmissionFactor._Cast_CarbonEmissionFactor"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CarbonEmissionFactor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CarbonEmissionFactor:
    """Special nested class for casting CarbonEmissionFactor to subclasses."""

    __parent__: "CarbonEmissionFactor"

    @property
    def measurement_base(self: "CastSelf") -> "_1797.MeasurementBase":
        return self.__parent__._cast(_1797.MeasurementBase)

    @property
    def carbon_emission_factor(self: "CastSelf") -> "CarbonEmissionFactor":
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
class CarbonEmissionFactor(_1797.MeasurementBase):
    """CarbonEmissionFactor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CARBON_EMISSION_FACTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CarbonEmissionFactor":
        """Cast to another type.

        Returns:
            _Cast_CarbonEmissionFactor
        """
        return _Cast_CarbonEmissionFactor(self)
