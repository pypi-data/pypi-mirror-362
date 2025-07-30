"""RaceRoundnessAtAngle"""

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

_RACE_ROUNDNESS_AT_ANGLE = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "RaceRoundnessAtAngle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RaceRoundnessAtAngle")
    CastSelf = TypeVar(
        "CastSelf", bound="RaceRoundnessAtAngle._Cast_RaceRoundnessAtAngle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RaceRoundnessAtAngle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RaceRoundnessAtAngle:
    """Special nested class for casting RaceRoundnessAtAngle to subclasses."""

    __parent__: "RaceRoundnessAtAngle"

    @property
    def race_roundness_at_angle(self: "CastSelf") -> "RaceRoundnessAtAngle":
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
class RaceRoundnessAtAngle(_0.APIBase):
    """RaceRoundnessAtAngle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RACE_ROUNDNESS_AT_ANGLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Angle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Deviation")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_RaceRoundnessAtAngle":
        """Cast to another type.

        Returns:
            _Cast_RaceRoundnessAtAngle
        """
        return _Cast_RaceRoundnessAtAngle(self)
