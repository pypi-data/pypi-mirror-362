"""RingTolerance"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.tolerances import _2112

_RING_TOLERANCE = python_net_import("SMT.MastaAPI.Bearings.Tolerances", "RingTolerance")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.tolerances import _2104, _2109, _2115, _2121

    Self = TypeVar("Self", bound="RingTolerance")
    CastSelf = TypeVar("CastSelf", bound="RingTolerance._Cast_RingTolerance")


__docformat__ = "restructuredtext en"
__all__ = ("RingTolerance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingTolerance:
    """Special nested class for casting RingTolerance to subclasses."""

    __parent__: "RingTolerance"

    @property
    def interference_tolerance(self: "CastSelf") -> "_2112.InterferenceTolerance":
        return self.__parent__._cast(_2112.InterferenceTolerance)

    @property
    def bearing_connection_component(
        self: "CastSelf",
    ) -> "_2104.BearingConnectionComponent":
        from mastapy._private.bearings.tolerances import _2104

        return self.__parent__._cast(_2104.BearingConnectionComponent)

    @property
    def inner_ring_tolerance(self: "CastSelf") -> "_2109.InnerRingTolerance":
        from mastapy._private.bearings.tolerances import _2109

        return self.__parent__._cast(_2109.InnerRingTolerance)

    @property
    def outer_ring_tolerance(self: "CastSelf") -> "_2115.OuterRingTolerance":
        from mastapy._private.bearings.tolerances import _2115

        return self.__parent__._cast(_2115.OuterRingTolerance)

    @property
    def ring_tolerance(self: "CastSelf") -> "RingTolerance":
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
class RingTolerance(_2112.InterferenceTolerance):
    """RingTolerance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_TOLERANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def roundness_specification(self: "Self") -> "_2121.RoundnessSpecification":
        """mastapy.bearings.tolerances.RoundnessSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoundnessSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RingTolerance":
        """Cast to another type.

        Returns:
            _Cast_RingTolerance
        """
        return _Cast_RingTolerance(self)
