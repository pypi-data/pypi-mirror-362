"""PlainGreaseFilledJournalBearingHousingType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PLAIN_GREASE_FILLED_JOURNAL_BEARING_HOUSING_TYPE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm",
    "PlainGreaseFilledJournalBearingHousingType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PlainGreaseFilledJournalBearingHousingType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlainGreaseFilledJournalBearingHousingType._Cast_PlainGreaseFilledJournalBearingHousingType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlainGreaseFilledJournalBearingHousingType",)


class PlainGreaseFilledJournalBearingHousingType(Enum):
    """PlainGreaseFilledJournalBearingHousingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PLAIN_GREASE_FILLED_JOURNAL_BEARING_HOUSING_TYPE

    MACHINERY_ENCASED = 0
    PEDESTAL_BASE = 1
    CYLINDRICAL_HOUSING = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


PlainGreaseFilledJournalBearingHousingType.__setattr__ = __enum_setattr
PlainGreaseFilledJournalBearingHousingType.__delattr__ = __enum_delattr
