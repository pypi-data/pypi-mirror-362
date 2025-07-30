"""LoadedLinearBearingResults"""

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
from mastapy._private.bearings.bearing_results import _2155

_LOADED_LINEAR_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedLinearBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2078

    Self = TypeVar("Self", bound="LoadedLinearBearingResults")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedLinearBearingResults._Cast_LoadedLinearBearingResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedLinearBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedLinearBearingResults:
    """Special nested class for casting LoadedLinearBearingResults to subclasses."""

    __parent__: "LoadedLinearBearingResults"

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2155.LoadedBearingResults":
        return self.__parent__._cast(_2155.LoadedBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_2078.BearingLoadCaseResultsLightweight":
        from mastapy._private.bearings import _2078

        return self.__parent__._cast(_2078.BearingLoadCaseResultsLightweight)

    @property
    def loaded_linear_bearing_results(self: "CastSelf") -> "LoadedLinearBearingResults":
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
class LoadedLinearBearingResults(_2155.LoadedBearingResults):
    """LoadedLinearBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_LINEAR_BEARING_RESULTS

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
    def cast_to(self: "Self") -> "_Cast_LoadedLinearBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedLinearBearingResults
        """
        return _Cast_LoadedLinearBearingResults(self)
