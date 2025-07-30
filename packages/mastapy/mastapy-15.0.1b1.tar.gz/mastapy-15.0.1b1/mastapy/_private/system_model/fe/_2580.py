"""AngleSource"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ANGLE_SOURCE = python_net_import("SMT.MastaAPI.SystemModel.FE", "AngleSource")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AngleSource")
    CastSelf = TypeVar("CastSelf", bound="AngleSource._Cast_AngleSource")


__docformat__ = "restructuredtext en"
__all__ = ("AngleSource",)


class AngleSource(Enum):
    """AngleSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ANGLE_SOURCE

    SPECIFIED_VALUE = 0
    DERIVED = 1
    INDEX = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AngleSource.__setattr__ = __enum_setattr
AngleSource.__delattr__ = __enum_delattr
