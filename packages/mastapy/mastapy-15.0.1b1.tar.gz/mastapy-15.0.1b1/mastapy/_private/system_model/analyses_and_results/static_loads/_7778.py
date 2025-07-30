"""InformationAtRingPinToDiscContactPointFromGeometry"""

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

_INFORMATION_AT_RING_PIN_TO_DISC_CONTACT_POINT_FROM_GEOMETRY = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "InformationAtRingPinToDiscContactPointFromGeometry",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InformationAtRingPinToDiscContactPointFromGeometry")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InformationAtRingPinToDiscContactPointFromGeometry._Cast_InformationAtRingPinToDiscContactPointFromGeometry",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InformationAtRingPinToDiscContactPointFromGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InformationAtRingPinToDiscContactPointFromGeometry:
    """Special nested class for casting InformationAtRingPinToDiscContactPointFromGeometry to subclasses."""

    __parent__: "InformationAtRingPinToDiscContactPointFromGeometry"

    @property
    def information_at_ring_pin_to_disc_contact_point_from_geometry(
        self: "CastSelf",
    ) -> "InformationAtRingPinToDiscContactPointFromGeometry":
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
class InformationAtRingPinToDiscContactPointFromGeometry(_0.APIBase):
    """InformationAtRingPinToDiscContactPointFromGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INFORMATION_AT_RING_PIN_TO_DISC_CONTACT_POINT_FROM_GEOMETRY
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def clearance_due_to_disc_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClearanceDueToDiscProfile")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def clearance_due_to_ring_pin_manufacturing_errors(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ClearanceDueToRingPinManufacturingErrors"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def combined_curvature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CombinedCurvature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def combined_radius_of_curvature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CombinedRadiusOfCurvature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def disc_radius_of_curvature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiscRadiusOfCurvature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normalised_arc_length_along_half_lobe_to_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedArcLengthAlongHalfLobeToContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pin_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinIndex")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def ring_pin_radius_of_curvature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingPinRadiusOfCurvature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_InformationAtRingPinToDiscContactPointFromGeometry":
        """Cast to another type.

        Returns:
            _Cast_InformationAtRingPinToDiscContactPointFromGeometry
        """
        return _Cast_InformationAtRingPinToDiscContactPointFromGeometry(self)
