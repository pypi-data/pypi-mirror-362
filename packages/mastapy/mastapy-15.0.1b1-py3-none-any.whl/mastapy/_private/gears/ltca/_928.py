"""ConicalGearFilletStressResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.ltca import _940

_CONICAL_GEAR_FILLET_STRESS_RESULTS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "ConicalGearFilletStressResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalGearFilletStressResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearFilletStressResults._Cast_ConicalGearFilletStressResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearFilletStressResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearFilletStressResults:
    """Special nested class for casting ConicalGearFilletStressResults to subclasses."""

    __parent__: "ConicalGearFilletStressResults"

    @property
    def gear_fillet_node_stress_results(
        self: "CastSelf",
    ) -> "_940.GearFilletNodeStressResults":
        return self.__parent__._cast(_940.GearFilletNodeStressResults)

    @property
    def conical_gear_fillet_stress_results(
        self: "CastSelf",
    ) -> "ConicalGearFilletStressResults":
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
class ConicalGearFilletStressResults(_940.GearFilletNodeStressResults):
    """ConicalGearFilletStressResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_FILLET_STRESS_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearFilletStressResults":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearFilletStressResults
        """
        return _Cast_ConicalGearFilletStressResults(self)
