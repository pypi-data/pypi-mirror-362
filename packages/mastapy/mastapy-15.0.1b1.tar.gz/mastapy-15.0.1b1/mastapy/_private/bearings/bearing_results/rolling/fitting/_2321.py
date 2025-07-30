"""OuterRingFittingThermalResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling.fitting import _2322

_OUTER_RING_FITTING_THERMAL_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.Fitting",
    "OuterRingFittingThermalResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OuterRingFittingThermalResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="OuterRingFittingThermalResults._Cast_OuterRingFittingThermalResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("OuterRingFittingThermalResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OuterRingFittingThermalResults:
    """Special nested class for casting OuterRingFittingThermalResults to subclasses."""

    __parent__: "OuterRingFittingThermalResults"

    @property
    def ring_fitting_thermal_results(
        self: "CastSelf",
    ) -> "_2322.RingFittingThermalResults":
        return self.__parent__._cast(_2322.RingFittingThermalResults)

    @property
    def outer_ring_fitting_thermal_results(
        self: "CastSelf",
    ) -> "OuterRingFittingThermalResults":
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
class OuterRingFittingThermalResults(_2322.RingFittingThermalResults):
    """OuterRingFittingThermalResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OUTER_RING_FITTING_THERMAL_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_OuterRingFittingThermalResults":
        """Cast to another type.

        Returns:
            _Cast_OuterRingFittingThermalResults
        """
        return _Cast_OuterRingFittingThermalResults(self)
