"""CylindricalGearScuffingResults"""

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

_CYLINDRICAL_GEAR_SCUFFING_RESULTS = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalGearScuffingResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical import _575

    Self = TypeVar("Self", bound="CylindricalGearScuffingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearScuffingResults._Cast_CylindricalGearScuffingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearScuffingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearScuffingResults:
    """Special nested class for casting CylindricalGearScuffingResults to subclasses."""

    __parent__: "CylindricalGearScuffingResults"

    @property
    def cylindrical_gear_scuffing_results(
        self: "CastSelf",
    ) -> "CylindricalGearScuffingResults":
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
class CylindricalGearScuffingResults(_0.APIBase):
    """CylindricalGearScuffingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SCUFFING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def scuffing_results_row(self: "Self") -> "List[_575.ScuffingResultsRow]":
        """List[mastapy.gears.rating.cylindrical.ScuffingResultsRow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingResultsRow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearScuffingResults":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearScuffingResults
        """
        return _Cast_CylindricalGearScuffingResults(self)
