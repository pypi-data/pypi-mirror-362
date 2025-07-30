"""LoadedTiltingJournalPad"""

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
from mastapy._private.bearings.bearing_results.fluid_film import _2328

_LOADED_TILTING_JOURNAL_PAD = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.FluidFilm", "LoadedTiltingJournalPad"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadedTiltingJournalPad")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedTiltingJournalPad._Cast_LoadedTiltingJournalPad"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedTiltingJournalPad",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedTiltingJournalPad:
    """Special nested class for casting LoadedTiltingJournalPad to subclasses."""

    __parent__: "LoadedTiltingJournalPad"

    @property
    def loaded_fluid_film_bearing_pad(
        self: "CastSelf",
    ) -> "_2328.LoadedFluidFilmBearingPad":
        return self.__parent__._cast(_2328.LoadedFluidFilmBearingPad)

    @property
    def loaded_tilting_journal_pad(self: "CastSelf") -> "LoadedTiltingJournalPad":
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
class LoadedTiltingJournalPad(_2328.LoadedFluidFilmBearingPad):
    """LoadedTiltingJournalPad

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_TILTING_JOURNAL_PAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def eccentricity_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EccentricityRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lubricant_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumLubricantFilmThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedTiltingJournalPad":
        """Cast to another type.

        Returns:
            _Cast_LoadedTiltingJournalPad
        """
        return _Cast_LoadedTiltingJournalPad(self)
