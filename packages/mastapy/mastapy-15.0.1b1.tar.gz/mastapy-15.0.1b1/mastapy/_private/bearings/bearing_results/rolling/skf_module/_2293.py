"""FrictionalMoment"""

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

_FRICTIONAL_MOMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "FrictionalMoment"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FrictionalMoment")
    CastSelf = TypeVar("CastSelf", bound="FrictionalMoment._Cast_FrictionalMoment")


__docformat__ = "restructuredtext en"
__all__ = ("FrictionalMoment",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FrictionalMoment:
    """Special nested class for casting FrictionalMoment to subclasses."""

    __parent__: "FrictionalMoment"

    @property
    def frictional_moment(self: "CastSelf") -> "FrictionalMoment":
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
class FrictionalMoment(_0.APIBase):
    """FrictionalMoment

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FRICTIONAL_MOMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def at_start_2030_degrees_c_and_zero_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AtStart2030DegreesCAndZeroSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Total")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_FrictionalMoment":
        """Cast to another type.

        Returns:
            _Cast_FrictionalMoment
        """
        return _Cast_FrictionalMoment(self)
