"""CylindricalGearMicroPittingResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_CYLINDRICAL_GEAR_MICRO_PITTING_RESULTS = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalGearMicroPittingResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical import _568

    Self = TypeVar("Self", bound="CylindricalGearMicroPittingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMicroPittingResults._Cast_CylindricalGearMicroPittingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMicroPittingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMicroPittingResults:
    """Special nested class for casting CylindricalGearMicroPittingResults to subclasses."""

    __parent__: "CylindricalGearMicroPittingResults"

    @property
    def cylindrical_gear_micro_pitting_results(
        self: "CastSelf",
    ) -> "CylindricalGearMicroPittingResults":
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
class CylindricalGearMicroPittingResults(_0.APIBase):
    """CylindricalGearMicroPittingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MICRO_PITTING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def micro_pitting_results_row(self: "Self") -> "List[_568.MicroPittingResultsRow]":
        """List[mastapy.gears.rating.cylindrical.MicroPittingResultsRow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicroPittingResultsRow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMicroPittingResults":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMicroPittingResults
        """
        return _Cast_CylindricalGearMicroPittingResults(self)
