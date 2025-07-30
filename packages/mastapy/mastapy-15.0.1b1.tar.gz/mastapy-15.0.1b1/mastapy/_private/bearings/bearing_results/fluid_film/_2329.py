"""LoadedFluidFilmBearingResults"""

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
from mastapy._private.bearings.bearing_results import _2160

_LOADED_FLUID_FILM_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.FluidFilm", "LoadedFluidFilmBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2078
    from mastapy._private.bearings.bearing_results import _2155, _2163
    from mastapy._private.bearings.bearing_results.fluid_film import (
        _2330,
        _2331,
        _2332,
        _2334,
        _2337,
        _2338,
    )

    Self = TypeVar("Self", bound="LoadedFluidFilmBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedFluidFilmBearingResults._Cast_LoadedFluidFilmBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedFluidFilmBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedFluidFilmBearingResults:
    """Special nested class for casting LoadedFluidFilmBearingResults to subclasses."""

    __parent__: "LoadedFluidFilmBearingResults"

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2160.LoadedDetailedBearingResults":
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
    ) -> "_2330.LoadedGreaseFilledJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2330

        return self.__parent__._cast(_2330.LoadedGreaseFilledJournalBearingResults)

    @property
    def loaded_pad_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2331.LoadedPadFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2331

        return self.__parent__._cast(_2331.LoadedPadFluidFilmBearingResults)

    @property
    def loaded_plain_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2332.LoadedPlainJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2332

        return self.__parent__._cast(_2332.LoadedPlainJournalBearingResults)

    @property
    def loaded_plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2334.LoadedPlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_results.fluid_film import _2334

        return self.__parent__._cast(_2334.LoadedPlainOilFedJournalBearing)

    @property
    def loaded_tilting_pad_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2337.LoadedTiltingPadJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2337

        return self.__parent__._cast(_2337.LoadedTiltingPadJournalBearingResults)

    @property
    def loaded_tilting_pad_thrust_bearing_results(
        self: "CastSelf",
    ) -> "_2338.LoadedTiltingPadThrustBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2338

        return self.__parent__._cast(_2338.LoadedTiltingPadThrustBearingResults)

    @property
    def loaded_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "LoadedFluidFilmBearingResults":
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
class LoadedFluidFilmBearingResults(_2160.LoadedDetailedBearingResults):
    """LoadedFluidFilmBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_FLUID_FILM_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def relative_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedFluidFilmBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedFluidFilmBearingResults
        """
        return _Cast_LoadedFluidFilmBearingResults(self)
