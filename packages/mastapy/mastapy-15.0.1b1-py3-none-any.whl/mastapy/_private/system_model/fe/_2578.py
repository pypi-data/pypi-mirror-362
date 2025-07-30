"""AlignmentMethodForRaceBearing"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ALIGNMENT_METHOD_FOR_RACE_BEARING = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "AlignmentMethodForRaceBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AlignmentMethodForRaceBearing")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AlignmentMethodForRaceBearing._Cast_AlignmentMethodForRaceBearing",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AlignmentMethodForRaceBearing",)


class AlignmentMethodForRaceBearing(Enum):
    """AlignmentMethodForRaceBearing

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ALIGNMENT_METHOD_FOR_RACE_BEARING

    MANUAL = 0
    DATUM = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AlignmentMethodForRaceBearing.__setattr__ = __enum_setattr
AlignmentMethodForRaceBearing.__delattr__ = __enum_delattr
