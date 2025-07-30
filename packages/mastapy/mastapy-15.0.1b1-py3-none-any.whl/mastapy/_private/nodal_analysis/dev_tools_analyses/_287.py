"""NoneSelectedAllOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_NONE_SELECTED_ALL_OPTION = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "NoneSelectedAllOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NoneSelectedAllOption")
    CastSelf = TypeVar(
        "CastSelf", bound="NoneSelectedAllOption._Cast_NoneSelectedAllOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("NoneSelectedAllOption",)


class NoneSelectedAllOption(Enum):
    """NoneSelectedAllOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _NONE_SELECTED_ALL_OPTION

    NONE = 0
    SELECTED = 1
    ALL = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


NoneSelectedAllOption.__setattr__ = __enum_setattr
NoneSelectedAllOption.__delattr__ = __enum_delattr
