"""ANSIABMA92015Results"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling.abma import _2327

_ANSIABMA92015_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.ABMA", "ANSIABMA92015Results"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
        _2315,
    )

    Self = TypeVar("Self", bound="ANSIABMA92015Results")
    CastSelf = TypeVar(
        "CastSelf", bound="ANSIABMA92015Results._Cast_ANSIABMA92015Results"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ANSIABMA92015Results",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ANSIABMA92015Results:
    """Special nested class for casting ANSIABMA92015Results to subclasses."""

    __parent__: "ANSIABMA92015Results"

    @property
    def ansiabma_results(self: "CastSelf") -> "_2327.ANSIABMAResults":
        return self.__parent__._cast(_2327.ANSIABMAResults)

    @property
    def iso_results(self: "CastSelf") -> "_2315.ISOResults":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2315,
        )

        return self.__parent__._cast(_2315.ISOResults)

    @property
    def ansiabma92015_results(self: "CastSelf") -> "ANSIABMA92015Results":
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
class ANSIABMA92015Results(_2327.ANSIABMAResults):
    """ANSIABMA92015Results

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ANSIABMA92015_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ANSIABMA92015Results":
        """Cast to another type.

        Returns:
            _Cast_ANSIABMA92015Results
        """
        return _Cast_ANSIABMA92015Results(self)
