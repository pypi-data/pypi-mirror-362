"""SafetyFactorGroup"""

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

_SAFETY_FACTOR_GROUP = python_net_import("SMT.MastaAPI.Materials", "SafetyFactorGroup")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.materials import _369

    Self = TypeVar("Self", bound="SafetyFactorGroup")
    CastSelf = TypeVar("CastSelf", bound="SafetyFactorGroup._Cast_SafetyFactorGroup")


__docformat__ = "restructuredtext en"
__all__ = ("SafetyFactorGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SafetyFactorGroup:
    """Special nested class for casting SafetyFactorGroup to subclasses."""

    __parent__: "SafetyFactorGroup"

    @property
    def safety_factor_group(self: "CastSelf") -> "SafetyFactorGroup":
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
class SafetyFactorGroup(_0.APIBase):
    """SafetyFactorGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SAFETY_FACTOR_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def items(self: "Self") -> "List[_369.SafetyFactorItem]":
        """List[mastapy.materials.SafetyFactorItem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Items")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SafetyFactorGroup":
        """Cast to another type.

        Returns:
            _Cast_SafetyFactorGroup
        """
        return _Cast_SafetyFactorGroup(self)
