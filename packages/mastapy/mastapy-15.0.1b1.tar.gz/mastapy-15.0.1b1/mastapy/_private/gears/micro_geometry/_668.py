"""MainProfileReliefEndsAtTheStartOfRootReliefOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MAIN_PROFILE_RELIEF_ENDS_AT_THE_START_OF_ROOT_RELIEF_OPTION = python_net_import(
    "SMT.MastaAPI.Gears.MicroGeometry",
    "MainProfileReliefEndsAtTheStartOfRootReliefOption",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MainProfileReliefEndsAtTheStartOfRootReliefOption")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MainProfileReliefEndsAtTheStartOfRootReliefOption._Cast_MainProfileReliefEndsAtTheStartOfRootReliefOption",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MainProfileReliefEndsAtTheStartOfRootReliefOption",)


class MainProfileReliefEndsAtTheStartOfRootReliefOption(Enum):
    """MainProfileReliefEndsAtTheStartOfRootReliefOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MAIN_PROFILE_RELIEF_ENDS_AT_THE_START_OF_ROOT_RELIEF_OPTION

    NO = 0
    YES = 1
    ONLY_WHEN_NON_ZERO_ROOT_RELIEF = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MainProfileReliefEndsAtTheStartOfRootReliefOption.__setattr__ = __enum_setattr
MainProfileReliefEndsAtTheStartOfRootReliefOption.__delattr__ = __enum_delattr
