"""LeadModificationSegment"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical import _739

_LEAD_MODIFICATION_SEGMENT = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "LeadModificationSegment"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LeadModificationSegment")
    CastSelf = TypeVar(
        "CastSelf", bound="LeadModificationSegment._Cast_LeadModificationSegment"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LeadModificationSegment",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LeadModificationSegment:
    """Special nested class for casting LeadModificationSegment to subclasses."""

    __parent__: "LeadModificationSegment"

    @property
    def modification_segment(self: "CastSelf") -> "_739.ModificationSegment":
        return self.__parent__._cast(_739.ModificationSegment)

    @property
    def lead_modification_segment(self: "CastSelf") -> "LeadModificationSegment":
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
class LeadModificationSegment(_739.ModificationSegment):
    """LeadModificationSegment

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LEAD_MODIFICATION_SEGMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def distance_from_centre(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DistanceFromCentre")

        if temp is None:
            return 0.0

        return temp

    @distance_from_centre.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_from_centre(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceFromCentre",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_LeadModificationSegment":
        """Cast to another type.

        Returns:
            _Cast_LeadModificationSegment
        """
        return _Cast_LeadModificationSegment(self)
