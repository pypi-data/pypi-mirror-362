"""RotationalFrequency"""

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

_ROTATIONAL_FREQUENCY = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "RotationalFrequency"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RotationalFrequency")
    CastSelf = TypeVar(
        "CastSelf", bound="RotationalFrequency._Cast_RotationalFrequency"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RotationalFrequency",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RotationalFrequency:
    """Special nested class for casting RotationalFrequency to subclasses."""

    __parent__: "RotationalFrequency"

    @property
    def rotational_frequency(self: "CastSelf") -> "RotationalFrequency":
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
class RotationalFrequency(_0.APIBase):
    """RotationalFrequency

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROTATIONAL_FREQUENCY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def inner_ring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_ring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rolling_element_about_its_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingElementAboutItsAxis")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rolling_element_set_and_cage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingElementSetAndCage")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_RotationalFrequency":
        """Cast to another type.

        Returns:
            _Cast_RotationalFrequency
        """
        return _Cast_RotationalFrequency(self)
