"""OuterRingTolerance"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.tolerances import _2120

_OUTER_RING_TOLERANCE = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "OuterRingTolerance"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.tolerances import _2104, _2112

    Self = TypeVar("Self", bound="OuterRingTolerance")
    CastSelf = TypeVar("CastSelf", bound="OuterRingTolerance._Cast_OuterRingTolerance")


__docformat__ = "restructuredtext en"
__all__ = ("OuterRingTolerance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OuterRingTolerance:
    """Special nested class for casting OuterRingTolerance to subclasses."""

    __parent__: "OuterRingTolerance"

    @property
    def ring_tolerance(self: "CastSelf") -> "_2120.RingTolerance":
        return self.__parent__._cast(_2120.RingTolerance)

    @property
    def interference_tolerance(self: "CastSelf") -> "_2112.InterferenceTolerance":
        from mastapy._private.bearings.tolerances import _2112

        return self.__parent__._cast(_2112.InterferenceTolerance)

    @property
    def bearing_connection_component(
        self: "CastSelf",
    ) -> "_2104.BearingConnectionComponent":
        from mastapy._private.bearings.tolerances import _2104

        return self.__parent__._cast(_2104.BearingConnectionComponent)

    @property
    def outer_ring_tolerance(self: "CastSelf") -> "OuterRingTolerance":
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
class OuterRingTolerance(_2120.RingTolerance):
    """OuterRingTolerance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OUTER_RING_TOLERANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_OuterRingTolerance":
        """Cast to another type.

        Returns:
            _Cast_OuterRingTolerance
        """
        return _Cast_OuterRingTolerance(self)
