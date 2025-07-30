"""ISOTR1417922001Results"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2187

_ISOTR1417922001_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "ISOTR1417922001Results"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ISOTR1417922001Results")
    CastSelf = TypeVar(
        "CastSelf", bound="ISOTR1417922001Results._Cast_ISOTR1417922001Results"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISOTR1417922001Results",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISOTR1417922001Results:
    """Special nested class for casting ISOTR1417922001Results to subclasses."""

    __parent__: "ISOTR1417922001Results"

    @property
    def isotr141792001_results(self: "CastSelf") -> "_2187.ISOTR141792001Results":
        return self.__parent__._cast(_2187.ISOTR141792001Results)

    @property
    def isotr1417922001_results(self: "CastSelf") -> "ISOTR1417922001Results":
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
class ISOTR1417922001Results(_2187.ISOTR141792001Results):
    """ISOTR1417922001Results

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISOTR1417922001_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def coefficient_for_no_load_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoefficientForNoLoadPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISOTR1417922001Results":
        """Cast to another type.

        Returns:
            _Cast_ISOTR1417922001Results
        """
        return _Cast_ISOTR1417922001Results(self)
