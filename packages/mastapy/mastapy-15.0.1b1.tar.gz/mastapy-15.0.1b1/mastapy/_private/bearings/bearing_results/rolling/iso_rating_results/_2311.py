"""BallISO2812007Results"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import _2313

_BALL_ISO2812007_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults",
    "BallISO2812007Results",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
        _2315,
    )

    Self = TypeVar("Self", bound="BallISO2812007Results")
    CastSelf = TypeVar(
        "CastSelf", bound="BallISO2812007Results._Cast_BallISO2812007Results"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BallISO2812007Results",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BallISO2812007Results:
    """Special nested class for casting BallISO2812007Results to subclasses."""

    __parent__: "BallISO2812007Results"

    @property
    def iso2812007_results(self: "CastSelf") -> "_2313.ISO2812007Results":
        return self.__parent__._cast(_2313.ISO2812007Results)

    @property
    def iso_results(self: "CastSelf") -> "_2315.ISOResults":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2315,
        )

        return self.__parent__._cast(_2315.ISOResults)

    @property
    def ball_iso2812007_results(self: "CastSelf") -> "BallISO2812007Results":
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
class BallISO2812007Results(_2313.ISO2812007Results):
    """BallISO2812007Results

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BALL_ISO2812007_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BallISO2812007Results":
        """Cast to another type.

        Returns:
            _Cast_BallISO2812007Results
        """
        return _Cast_BallISO2812007Results(self)
