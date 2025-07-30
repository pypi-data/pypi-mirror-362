"""MaxMinMean"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MAX_MIN_MEAN = python_net_import("SMT.MastaAPI.MathUtility", "MaxMinMean")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MaxMinMean")
    CastSelf = TypeVar("CastSelf", bound="MaxMinMean._Cast_MaxMinMean")


__docformat__ = "restructuredtext en"
__all__ = ("MaxMinMean",)


class MaxMinMean(Enum):
    """MaxMinMean

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MAX_MIN_MEAN

    MAX = 0
    MIN = 1
    MEAN = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MaxMinMean.__setattr__ = __enum_setattr
MaxMinMean.__delattr__ = __enum_delattr
