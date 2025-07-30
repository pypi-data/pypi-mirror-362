"""IndependentResistiveTorque"""

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
from mastapy._private.materials.efficiency import _392

_INDEPENDENT_RESISTIVE_TORQUE = python_net_import(
    "SMT.MastaAPI.Materials.Efficiency", "IndependentResistiveTorque"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="IndependentResistiveTorque")
    CastSelf = TypeVar(
        "CastSelf", bound="IndependentResistiveTorque._Cast_IndependentResistiveTorque"
    )


__docformat__ = "restructuredtext en"
__all__ = ("IndependentResistiveTorque",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_IndependentResistiveTorque:
    """Special nested class for casting IndependentResistiveTorque to subclasses."""

    __parent__: "IndependentResistiveTorque"

    @property
    def resistive_torque(self: "CastSelf") -> "_392.ResistiveTorque":
        return self.__parent__._cast(_392.ResistiveTorque)

    @property
    def independent_resistive_torque(self: "CastSelf") -> "IndependentResistiveTorque":
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
class IndependentResistiveTorque(_392.ResistiveTorque):
    """IndependentResistiveTorque

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INDEPENDENT_RESISTIVE_TORQUE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def load_dependent_resistive_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDependentResistiveTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def speed_dependent_resistive_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedDependentResistiveTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_IndependentResistiveTorque":
        """Cast to another type.

        Returns:
            _Cast_IndependentResistiveTorque
        """
        return _Cast_IndependentResistiveTorque(self)
