"""WorkingCharacteristics"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_WORKING_CHARACTERISTICS = python_net_import(
    "SMT.MastaAPI.Materials", "WorkingCharacteristics"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WorkingCharacteristics")
    CastSelf = TypeVar(
        "CastSelf", bound="WorkingCharacteristics._Cast_WorkingCharacteristics"
    )


__docformat__ = "restructuredtext en"
__all__ = ("WorkingCharacteristics",)


class WorkingCharacteristics(Enum):
    """WorkingCharacteristics

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _WORKING_CHARACTERISTICS

    UNIFORM = 0
    LIGHT_SHOCKS = 1
    MODERATE_SHOCKS = 2
    HEAVY_SHOCKS = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


WorkingCharacteristics.__setattr__ = __enum_setattr
WorkingCharacteristics.__delattr__ = __enum_delattr
