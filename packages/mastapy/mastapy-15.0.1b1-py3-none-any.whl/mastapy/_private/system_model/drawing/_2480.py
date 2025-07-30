"""StressResultOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_STRESS_RESULT_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "StressResultOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="StressResultOption")
    CastSelf = TypeVar("CastSelf", bound="StressResultOption._Cast_StressResultOption")


__docformat__ = "restructuredtext en"
__all__ = ("StressResultOption",)


class StressResultOption(Enum):
    """StressResultOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _STRESS_RESULT_OPTION

    ELEMENT_NODE = 0
    AVERAGE_TO_NODES = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


StressResultOption.__setattr__ = __enum_setattr
StressResultOption.__delattr__ = __enum_delattr
