"""ISOTR1417912001Results"""

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

_ISOTR1417912001_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "ISOTR1417912001Results"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ISOTR1417912001Results")
    CastSelf = TypeVar(
        "CastSelf", bound="ISOTR1417912001Results._Cast_ISOTR1417912001Results"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISOTR1417912001Results",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISOTR1417912001Results:
    """Special nested class for casting ISOTR1417912001Results to subclasses."""

    __parent__: "ISOTR1417912001Results"

    @property
    def isotr141792001_results(self: "CastSelf") -> "_2187.ISOTR141792001Results":
        return self.__parent__._cast(_2187.ISOTR141792001Results)

    @property
    def isotr1417912001_results(self: "CastSelf") -> "ISOTR1417912001Results":
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
class ISOTR1417912001Results(_2187.ISOTR141792001Results):
    """ISOTR1417912001Results

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISOTR1417912001_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bearing_dip_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingDipFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bearing_dip_factor_max(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingDipFactorMax")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bearing_dip_factor_min(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingDipFactorMin")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def frictional_moment_of_the_bearing_seal(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionalMomentOfTheBearingSeal")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISOTR1417912001Results":
        """Cast to another type.

        Returns:
            _Cast_ISOTR1417912001Results
        """
        return _Cast_ISOTR1417912001Results(self)
