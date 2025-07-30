"""StressAtPosition"""

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

_STRESS_AT_POSITION = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "StressAtPosition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="StressAtPosition")
    CastSelf = TypeVar("CastSelf", bound="StressAtPosition._Cast_StressAtPosition")


__docformat__ = "restructuredtext en"
__all__ = ("StressAtPosition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StressAtPosition:
    """Special nested class for casting StressAtPosition to subclasses."""

    __parent__: "StressAtPosition"

    @property
    def stress_at_position(self: "CastSelf") -> "StressAtPosition":
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
class StressAtPosition(_0.APIBase):
    """StressAtPosition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRESS_AT_POSITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def position(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Position")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Stress")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_StressAtPosition":
        """Cast to another type.

        Returns:
            _Cast_StressAtPosition
        """
        return _Cast_StressAtPosition(self)
