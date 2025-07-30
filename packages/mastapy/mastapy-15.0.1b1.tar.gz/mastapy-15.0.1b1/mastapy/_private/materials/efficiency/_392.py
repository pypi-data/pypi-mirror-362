"""ResistiveTorque"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_RESISTIVE_TORQUE = python_net_import(
    "SMT.MastaAPI.Materials.Efficiency", "ResistiveTorque"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.materials.efficiency import _383, _385

    Self = TypeVar("Self", bound="ResistiveTorque")
    CastSelf = TypeVar("CastSelf", bound="ResistiveTorque._Cast_ResistiveTorque")


__docformat__ = "restructuredtext en"
__all__ = ("ResistiveTorque",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResistiveTorque:
    """Special nested class for casting ResistiveTorque to subclasses."""

    __parent__: "ResistiveTorque"

    @property
    def combined_resistive_torque(self: "CastSelf") -> "_383.CombinedResistiveTorque":
        from mastapy._private.materials.efficiency import _383

        return self.__parent__._cast(_383.CombinedResistiveTorque)

    @property
    def independent_resistive_torque(
        self: "CastSelf",
    ) -> "_385.IndependentResistiveTorque":
        from mastapy._private.materials.efficiency import _385

        return self.__parent__._cast(_385.IndependentResistiveTorque)

    @property
    def resistive_torque(self: "CastSelf") -> "ResistiveTorque":
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
class ResistiveTorque(_0.APIBase):
    """ResistiveTorque

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESISTIVE_TORQUE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def total_resistive_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalResistiveTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ResistiveTorque":
        """Cast to another type.

        Returns:
            _Cast_ResistiveTorque
        """
        return _Cast_ResistiveTorque(self)
