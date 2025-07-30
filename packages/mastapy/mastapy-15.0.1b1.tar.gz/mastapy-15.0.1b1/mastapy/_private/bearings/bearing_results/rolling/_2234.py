"""LoadedNonBarrelRollerBearingStripLoadResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2239

_LOADED_NON_BARREL_ROLLER_BEARING_STRIP_LOAD_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedNonBarrelRollerBearingStripLoadResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadedNonBarrelRollerBearingStripLoadResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedNonBarrelRollerBearingStripLoadResults._Cast_LoadedNonBarrelRollerBearingStripLoadResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedNonBarrelRollerBearingStripLoadResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedNonBarrelRollerBearingStripLoadResults:
    """Special nested class for casting LoadedNonBarrelRollerBearingStripLoadResults to subclasses."""

    __parent__: "LoadedNonBarrelRollerBearingStripLoadResults"

    @property
    def loaded_roller_strip_load_results(
        self: "CastSelf",
    ) -> "_2239.LoadedRollerStripLoadResults":
        return self.__parent__._cast(_2239.LoadedRollerStripLoadResults)

    @property
    def loaded_non_barrel_roller_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "LoadedNonBarrelRollerBearingStripLoadResults":
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
class LoadedNonBarrelRollerBearingStripLoadResults(_2239.LoadedRollerStripLoadResults):
    """LoadedNonBarrelRollerBearingStripLoadResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_NON_BARREL_ROLLER_BEARING_STRIP_LOAD_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedNonBarrelRollerBearingStripLoadResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedNonBarrelRollerBearingStripLoadResults
        """
        return _Cast_LoadedNonBarrelRollerBearingStripLoadResults(self)
