"""DefinitionBooleanCheckOptions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DEFINITION_BOOLEAN_CHECK_OPTIONS = python_net_import(
    "SMT.MastaAPI.Utility.Report", "DefinitionBooleanCheckOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DefinitionBooleanCheckOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DefinitionBooleanCheckOptions._Cast_DefinitionBooleanCheckOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DefinitionBooleanCheckOptions",)


class DefinitionBooleanCheckOptions(Enum):
    """DefinitionBooleanCheckOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DEFINITION_BOOLEAN_CHECK_OPTIONS

    NONE = 0
    INCLUDE_IF = 1
    EXCLUDE_IF = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DefinitionBooleanCheckOptions.__setattr__ = __enum_setattr
DefinitionBooleanCheckOptions.__delattr__ = __enum_delattr
