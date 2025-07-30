"""BearingToleranceDefinitionOptions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_TOLERANCE_DEFINITION_OPTIONS = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "BearingToleranceDefinitionOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingToleranceDefinitionOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BearingToleranceDefinitionOptions._Cast_BearingToleranceDefinitionOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingToleranceDefinitionOptions",)


class BearingToleranceDefinitionOptions(Enum):
    """BearingToleranceDefinitionOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_TOLERANCE_DEFINITION_OPTIONS

    CLASSES = 0
    VALUES = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingToleranceDefinitionOptions.__setattr__ = __enum_setattr
BearingToleranceDefinitionOptions.__delattr__ = __enum_delattr
