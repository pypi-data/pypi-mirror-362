"""RollerISO179562025Results"""

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
from mastapy._private.bearings.bearing_results.rolling import _2185

_ROLLER_ISO179562025_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "RollerISO179562025Results"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RollerISO179562025Results")
    CastSelf = TypeVar(
        "CastSelf", bound="RollerISO179562025Results._Cast_RollerISO179562025Results"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerISO179562025Results",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerISO179562025Results:
    """Special nested class for casting RollerISO179562025Results to subclasses."""

    __parent__: "RollerISO179562025Results"

    @property
    def iso179562025_results(self: "CastSelf") -> "_2185.ISO179562025Results":
        return self.__parent__._cast(_2185.ISO179562025Results)

    @property
    def roller_iso179562025_results(self: "CastSelf") -> "RollerISO179562025Results":
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
class RollerISO179562025Results(_2185.ISO179562025Results):
    """RollerISO179562025Results

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_ISO179562025_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_lamina_load_of_any_rolling_element_in_the_bearing(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumLaminaLoadOfAnyRollingElementInTheBearing"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_RollerISO179562025Results":
        """Cast to another type.

        Returns:
            _Cast_RollerISO179562025Results
        """
        return _Cast_RollerISO179562025Results(self)
