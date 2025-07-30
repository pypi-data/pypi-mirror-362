"""ThreePointContactInternalClearance"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2180

_THREE_POINT_CONTACT_INTERNAL_CLEARANCE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "ThreePointContactInternalClearance"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ThreePointContactInternalClearance")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ThreePointContactInternalClearance._Cast_ThreePointContactInternalClearance",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThreePointContactInternalClearance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThreePointContactInternalClearance:
    """Special nested class for casting ThreePointContactInternalClearance to subclasses."""

    __parent__: "ThreePointContactInternalClearance"

    @property
    def internal_clearance(self: "CastSelf") -> "_2180.InternalClearance":
        return self.__parent__._cast(_2180.InternalClearance)

    @property
    def three_point_contact_internal_clearance(
        self: "CastSelf",
    ) -> "ThreePointContactInternalClearance":
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
class ThreePointContactInternalClearance(_2180.InternalClearance):
    """ThreePointContactInternalClearance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THREE_POINT_CONTACT_INTERNAL_CLEARANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def operating_free_contact_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingFreeContactAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ThreePointContactInternalClearance":
        """Cast to another type.

        Returns:
            _Cast_ThreePointContactInternalClearance
        """
        return _Cast_ThreePointContactInternalClearance(self)
