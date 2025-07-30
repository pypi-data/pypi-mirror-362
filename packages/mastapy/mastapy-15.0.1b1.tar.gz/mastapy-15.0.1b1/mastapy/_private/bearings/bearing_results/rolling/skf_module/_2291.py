"""FrequencyOfOverRolling"""

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

_FREQUENCY_OF_OVER_ROLLING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "FrequencyOfOverRolling"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FrequencyOfOverRolling")
    CastSelf = TypeVar(
        "CastSelf", bound="FrequencyOfOverRolling._Cast_FrequencyOfOverRolling"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FrequencyOfOverRolling",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FrequencyOfOverRolling:
    """Special nested class for casting FrequencyOfOverRolling to subclasses."""

    __parent__: "FrequencyOfOverRolling"

    @property
    def frequency_of_over_rolling(self: "CastSelf") -> "FrequencyOfOverRolling":
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
class FrequencyOfOverRolling(_0.APIBase):
    """FrequencyOfOverRolling

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FREQUENCY_OF_OVER_ROLLING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def point_on_inner_ring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointOnInnerRing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def point_on_outer_ring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointOnOuterRing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rolling_element(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingElement")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_FrequencyOfOverRolling":
        """Cast to another type.

        Returns:
            _Cast_FrequencyOfOverRolling
        """
        return _Cast_FrequencyOfOverRolling(self)
