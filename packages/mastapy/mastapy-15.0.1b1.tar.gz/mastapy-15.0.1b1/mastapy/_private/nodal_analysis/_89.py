"""ResultLoggingFrequency"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RESULT_LOGGING_FREQUENCY = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "ResultLoggingFrequency"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ResultLoggingFrequency")
    CastSelf = TypeVar(
        "CastSelf", bound="ResultLoggingFrequency._Cast_ResultLoggingFrequency"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultLoggingFrequency",)


class ResultLoggingFrequency(Enum):
    """ResultLoggingFrequency

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RESULT_LOGGING_FREQUENCY

    ALL = 0
    IGNORE_SMALL_STEPS = 1
    NONE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ResultLoggingFrequency.__setattr__ = __enum_setattr
ResultLoggingFrequency.__delattr__ = __enum_delattr
