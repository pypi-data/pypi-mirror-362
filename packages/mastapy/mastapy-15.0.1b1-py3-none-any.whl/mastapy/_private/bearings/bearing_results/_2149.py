"""DefaultOrUserInput"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DEFAULT_OR_USER_INPUT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "DefaultOrUserInput"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DefaultOrUserInput")
    CastSelf = TypeVar("CastSelf", bound="DefaultOrUserInput._Cast_DefaultOrUserInput")


__docformat__ = "restructuredtext en"
__all__ = ("DefaultOrUserInput",)


class DefaultOrUserInput(Enum):
    """DefaultOrUserInput

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DEFAULT_OR_USER_INPUT

    DIN_STANDARD_DEFAULT = 0
    USERSPECIFIED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DefaultOrUserInput.__setattr__ = __enum_setattr
DefaultOrUserInput.__delattr__ = __enum_delattr
