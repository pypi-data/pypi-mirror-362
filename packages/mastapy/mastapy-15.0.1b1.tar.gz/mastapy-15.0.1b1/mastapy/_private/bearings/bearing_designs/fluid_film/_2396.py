"""CylindricalHousingJournalBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs.fluid_film import _2403

_CYLINDRICAL_HOUSING_JOURNAL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm", "CylindricalHousingJournalBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalHousingJournalBearing")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalHousingJournalBearing._Cast_CylindricalHousingJournalBearing",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalHousingJournalBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalHousingJournalBearing:
    """Special nested class for casting CylindricalHousingJournalBearing to subclasses."""

    __parent__: "CylindricalHousingJournalBearing"

    @property
    def plain_journal_housing(self: "CastSelf") -> "_2403.PlainJournalHousing":
        return self.__parent__._cast(_2403.PlainJournalHousing)

    @property
    def cylindrical_housing_journal_bearing(
        self: "CastSelf",
    ) -> "CylindricalHousingJournalBearing":
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
class CylindricalHousingJournalBearing(_2403.PlainJournalHousing):
    """CylindricalHousingJournalBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_HOUSING_JOURNAL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalHousingJournalBearing":
        """Cast to another type.

        Returns:
            _Cast_CylindricalHousingJournalBearing
        """
        return _Cast_CylindricalHousingJournalBearing(self)
