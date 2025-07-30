"""ISO10300RatingMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ISO10300_RATING_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ISO10300RatingMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ISO10300RatingMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="ISO10300RatingMethod._Cast_ISO10300RatingMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO10300RatingMethod",)


class ISO10300RatingMethod(Enum):
    """ISO10300RatingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ISO10300_RATING_METHOD

    METHOD_B1 = 0
    METHOD_B2 = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ISO10300RatingMethod.__setattr__ = __enum_setattr
ISO10300RatingMethod.__delattr__ = __enum_delattr
