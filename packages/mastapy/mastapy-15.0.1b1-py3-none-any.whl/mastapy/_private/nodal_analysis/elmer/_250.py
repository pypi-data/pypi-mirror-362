"""ElmerResultEntityType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ELMER_RESULT_ENTITY_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.Elmer", "ElmerResultEntityType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElmerResultEntityType")
    CastSelf = TypeVar(
        "CastSelf", bound="ElmerResultEntityType._Cast_ElmerResultEntityType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElmerResultEntityType",)


class ElmerResultEntityType(Enum):
    """ElmerResultEntityType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ELMER_RESULT_ENTITY_TYPE

    ELEMENT = 0
    NODE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ElmerResultEntityType.__setattr__ = __enum_setattr
ElmerResultEntityType.__delattr__ = __enum_delattr
