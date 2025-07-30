"""BearingF0InputMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_F0_INPUT_METHOD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "BearingF0InputMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingF0InputMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingF0InputMethod._Cast_BearingF0InputMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingF0InputMethod",)


class BearingF0InputMethod(Enum):
    """BearingF0InputMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_F0_INPUT_METHOD

    F0_DIRECTLY = 0
    FORCE_AND_DISPLACEMENT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingF0InputMethod.__setattr__ = __enum_setattr
BearingF0InputMethod.__delattr__ = __enum_delattr
