"""RingDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.tolerances import _2111

_RING_DETAIL = python_net_import("SMT.MastaAPI.Bearings.Tolerances", "RingDetail")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.tolerances import _2104

    Self = TypeVar("Self", bound="RingDetail")
    CastSelf = TypeVar("CastSelf", bound="RingDetail._Cast_RingDetail")


__docformat__ = "restructuredtext en"
__all__ = ("RingDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingDetail:
    """Special nested class for casting RingDetail to subclasses."""

    __parent__: "RingDetail"

    @property
    def interference_detail(self: "CastSelf") -> "_2111.InterferenceDetail":
        return self.__parent__._cast(_2111.InterferenceDetail)

    @property
    def bearing_connection_component(
        self: "CastSelf",
    ) -> "_2104.BearingConnectionComponent":
        from mastapy._private.bearings.tolerances import _2104

        return self.__parent__._cast(_2104.BearingConnectionComponent)

    @property
    def ring_detail(self: "CastSelf") -> "RingDetail":
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
class RingDetail(_2111.InterferenceDetail):
    """RingDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RingDetail":
        """Cast to another type.

        Returns:
            _Cast_RingDetail
        """
        return _Cast_RingDetail(self)
