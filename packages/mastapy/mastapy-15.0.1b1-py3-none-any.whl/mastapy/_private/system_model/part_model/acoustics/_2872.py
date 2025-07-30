"""CacheMemoryEstimates"""

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

_CACHE_MEMORY_ESTIMATES = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "CacheMemoryEstimates"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CacheMemoryEstimates")
    CastSelf = TypeVar(
        "CastSelf", bound="CacheMemoryEstimates._Cast_CacheMemoryEstimates"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CacheMemoryEstimates",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CacheMemoryEstimates:
    """Special nested class for casting CacheMemoryEstimates to subclasses."""

    __parent__: "CacheMemoryEstimates"

    @property
    def cache_memory_estimates(self: "CastSelf") -> "CacheMemoryEstimates":
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
class CacheMemoryEstimates(_0.APIBase):
    """CacheMemoryEstimates

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CACHE_MEMORY_ESTIMATES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def at_the_maximum_frequency(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AtTheMaximumFrequency")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def at_the_minimum_frequency(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AtTheMinimumFrequency")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def upper_bound_for_total_estimate(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UpperBoundForTotalEstimate")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_CacheMemoryEstimates":
        """Cast to another type.

        Returns:
            _Cast_CacheMemoryEstimates
        """
        return _Cast_CacheMemoryEstimates(self)
