"""AxialHoleJournalBearing"""

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
from mastapy._private.bearings.bearing_designs.fluid_film import _2392

_AXIAL_HOLE_JOURNAL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm", "AxialHoleJournalBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AxialHoleJournalBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="AxialHoleJournalBearing._Cast_AxialHoleJournalBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AxialHoleJournalBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AxialHoleJournalBearing:
    """Special nested class for casting AxialHoleJournalBearing to subclasses."""

    __parent__: "AxialHoleJournalBearing"

    @property
    def axial_feed_journal_bearing(self: "CastSelf") -> "_2392.AxialFeedJournalBearing":
        return self.__parent__._cast(_2392.AxialFeedJournalBearing)

    @property
    def axial_hole_journal_bearing(self: "CastSelf") -> "AxialHoleJournalBearing":
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
class AxialHoleJournalBearing(_2392.AxialFeedJournalBearing):
    """AxialHoleJournalBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AXIAL_HOLE_JOURNAL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def hole_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HoleDiameter")

        if temp is None:
            return 0.0

        return temp

    @hole_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def hole_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HoleDiameter", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AxialHoleJournalBearing":
        """Cast to another type.

        Returns:
            _Cast_AxialHoleJournalBearing
        """
        return _Cast_AxialHoleJournalBearing(self)
