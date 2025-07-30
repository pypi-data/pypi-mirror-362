"""InputSignalFilterLevel"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_INPUT_SIGNAL_FILTER_LEVEL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses", "InputSignalFilterLevel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InputSignalFilterLevel")
    CastSelf = TypeVar(
        "CastSelf", bound="InputSignalFilterLevel._Cast_InputSignalFilterLevel"
    )


__docformat__ = "restructuredtext en"
__all__ = ("InputSignalFilterLevel",)


class InputSignalFilterLevel(Enum):
    """InputSignalFilterLevel

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _INPUT_SIGNAL_FILTER_LEVEL

    NONE = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


InputSignalFilterLevel.__setattr__ = __enum_setattr
InputSignalFilterLevel.__delattr__ = __enum_delattr
