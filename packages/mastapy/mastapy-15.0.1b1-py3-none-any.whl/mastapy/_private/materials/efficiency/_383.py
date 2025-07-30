"""CombinedResistiveTorque"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.materials.efficiency import _392

_COMBINED_RESISTIVE_TORQUE = python_net_import(
    "SMT.MastaAPI.Materials.Efficiency", "CombinedResistiveTorque"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CombinedResistiveTorque")
    CastSelf = TypeVar(
        "CastSelf", bound="CombinedResistiveTorque._Cast_CombinedResistiveTorque"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CombinedResistiveTorque",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CombinedResistiveTorque:
    """Special nested class for casting CombinedResistiveTorque to subclasses."""

    __parent__: "CombinedResistiveTorque"

    @property
    def resistive_torque(self: "CastSelf") -> "_392.ResistiveTorque":
        return self.__parent__._cast(_392.ResistiveTorque)

    @property
    def combined_resistive_torque(self: "CastSelf") -> "CombinedResistiveTorque":
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
class CombinedResistiveTorque(_392.ResistiveTorque):
    """CombinedResistiveTorque

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMBINED_RESISTIVE_TORQUE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CombinedResistiveTorque":
        """Cast to another type.

        Returns:
            _Cast_CombinedResistiveTorque
        """
        return _Cast_CombinedResistiveTorque(self)
