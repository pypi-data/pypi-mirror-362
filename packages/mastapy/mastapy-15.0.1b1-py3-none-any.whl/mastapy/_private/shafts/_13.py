"""FkmVersionOfMinersRule"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FKM_VERSION_OF_MINERS_RULE = python_net_import(
    "SMT.MastaAPI.Shafts", "FkmVersionOfMinersRule"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FkmVersionOfMinersRule")
    CastSelf = TypeVar(
        "CastSelf", bound="FkmVersionOfMinersRule._Cast_FkmVersionOfMinersRule"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FkmVersionOfMinersRule",)


class FkmVersionOfMinersRule(Enum):
    """FkmVersionOfMinersRule

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FKM_VERSION_OF_MINERS_RULE

    CONSISTENT = 0
    ELEMENTARY = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FkmVersionOfMinersRule.__setattr__ = __enum_setattr
FkmVersionOfMinersRule.__delattr__ = __enum_delattr
