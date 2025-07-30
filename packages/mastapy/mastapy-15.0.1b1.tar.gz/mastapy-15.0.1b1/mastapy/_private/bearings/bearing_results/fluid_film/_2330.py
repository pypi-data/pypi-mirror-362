"""LoadedGreaseFilledJournalBearingResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.fluid_film import _2332

_LOADED_GREASE_FILLED_JOURNAL_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.FluidFilm",
    "LoadedGreaseFilledJournalBearingResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2078
    from mastapy._private.bearings.bearing_results import _2155, _2160, _2163
    from mastapy._private.bearings.bearing_results.fluid_film import _2329

    Self = TypeVar("Self", bound="LoadedGreaseFilledJournalBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedGreaseFilledJournalBearingResults._Cast_LoadedGreaseFilledJournalBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedGreaseFilledJournalBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedGreaseFilledJournalBearingResults:
    """Special nested class for casting LoadedGreaseFilledJournalBearingResults to subclasses."""

    __parent__: "LoadedGreaseFilledJournalBearingResults"

    @property
    def loaded_plain_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2332.LoadedPlainJournalBearingResults":
        return self.__parent__._cast(_2332.LoadedPlainJournalBearingResults)

    @property
    def loaded_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2329.LoadedFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2329

        return self.__parent__._cast(_2329.LoadedFluidFilmBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2160.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2160

        return self.__parent__._cast(_2160.LoadedDetailedBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2163.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2163

        return self.__parent__._cast(_2163.LoadedNonLinearBearingResults)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2155.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2155

        return self.__parent__._cast(_2155.LoadedBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_2078.BearingLoadCaseResultsLightweight":
        from mastapy._private.bearings import _2078

        return self.__parent__._cast(_2078.BearingLoadCaseResultsLightweight)

    @property
    def loaded_grease_filled_journal_bearing_results(
        self: "CastSelf",
    ) -> "LoadedGreaseFilledJournalBearingResults":
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
class LoadedGreaseFilledJournalBearingResults(_2332.LoadedPlainJournalBearingResults):
    """LoadedGreaseFilledJournalBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_GREASE_FILLED_JOURNAL_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedGreaseFilledJournalBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedGreaseFilledJournalBearingResults
        """
        return _Cast_LoadedGreaseFilledJournalBearingResults(self)
