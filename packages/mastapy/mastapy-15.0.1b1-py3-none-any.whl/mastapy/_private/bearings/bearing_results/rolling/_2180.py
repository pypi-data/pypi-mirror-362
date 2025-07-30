"""InternalClearance"""

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

_INTERNAL_CLEARANCE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "InternalClearance"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2283

    Self = TypeVar("Self", bound="InternalClearance")
    CastSelf = TypeVar("CastSelf", bound="InternalClearance._Cast_InternalClearance")


__docformat__ = "restructuredtext en"
__all__ = ("InternalClearance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InternalClearance:
    """Special nested class for casting InternalClearance to subclasses."""

    __parent__: "InternalClearance"

    @property
    def three_point_contact_internal_clearance(
        self: "CastSelf",
    ) -> "_2283.ThreePointContactInternalClearance":
        from mastapy._private.bearings.bearing_results.rolling import _2283

        return self.__parent__._cast(_2283.ThreePointContactInternalClearance)

    @property
    def internal_clearance(self: "CastSelf") -> "InternalClearance":
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
class InternalClearance(_0.APIBase):
    """InternalClearance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTERNAL_CLEARANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Axial")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Radial")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_InternalClearance":
        """Cast to another type.

        Returns:
            _Cast_InternalClearance
        """
        return _Cast_InternalClearance(self)
