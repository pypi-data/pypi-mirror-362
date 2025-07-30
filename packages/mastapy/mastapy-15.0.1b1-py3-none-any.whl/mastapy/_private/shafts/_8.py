"""ConsequenceOfFailure"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CONSEQUENCE_OF_FAILURE = python_net_import(
    "SMT.MastaAPI.Shafts", "ConsequenceOfFailure"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConsequenceOfFailure")
    CastSelf = TypeVar(
        "CastSelf", bound="ConsequenceOfFailure._Cast_ConsequenceOfFailure"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConsequenceOfFailure",)


class ConsequenceOfFailure(Enum):
    """ConsequenceOfFailure

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CONSEQUENCE_OF_FAILURE

    SEVERE = 0
    MEAN = 1
    MODERATE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ConsequenceOfFailure.__setattr__ = __enum_setattr
ConsequenceOfFailure.__delattr__ = __enum_delattr
