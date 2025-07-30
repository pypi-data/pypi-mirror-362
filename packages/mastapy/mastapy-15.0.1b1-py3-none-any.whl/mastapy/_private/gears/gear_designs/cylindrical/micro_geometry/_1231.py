"""LeadSlopeReliefWithDeviation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1230

_LEAD_SLOPE_RELIEF_WITH_DEVIATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "LeadSlopeReliefWithDeviation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1246

    Self = TypeVar("Self", bound="LeadSlopeReliefWithDeviation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LeadSlopeReliefWithDeviation._Cast_LeadSlopeReliefWithDeviation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LeadSlopeReliefWithDeviation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LeadSlopeReliefWithDeviation:
    """Special nested class for casting LeadSlopeReliefWithDeviation to subclasses."""

    __parent__: "LeadSlopeReliefWithDeviation"

    @property
    def lead_relief_with_deviation(self: "CastSelf") -> "_1230.LeadReliefWithDeviation":
        return self.__parent__._cast(_1230.LeadReliefWithDeviation)

    @property
    def relief_with_deviation(self: "CastSelf") -> "_1246.ReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1246

        return self.__parent__._cast(_1246.ReliefWithDeviation)

    @property
    def lead_slope_relief_with_deviation(
        self: "CastSelf",
    ) -> "LeadSlopeReliefWithDeviation":
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
class LeadSlopeReliefWithDeviation(_1230.LeadReliefWithDeviation):
    """LeadSlopeReliefWithDeviation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LEAD_SLOPE_RELIEF_WITH_DEVIATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LeadSlopeReliefWithDeviation":
        """Cast to another type.

        Returns:
            _Cast_LeadSlopeReliefWithDeviation
        """
        return _Cast_LeadSlopeReliefWithDeviation(self)
