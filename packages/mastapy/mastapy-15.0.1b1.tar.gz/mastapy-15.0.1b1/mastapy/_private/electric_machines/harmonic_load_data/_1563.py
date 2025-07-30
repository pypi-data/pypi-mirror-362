"""ForceDisplayOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FORCE_DISPLAY_OPTION = python_net_import(
    "SMT.MastaAPI.ElectricMachines.HarmonicLoadData", "ForceDisplayOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ForceDisplayOption")
    CastSelf = TypeVar("CastSelf", bound="ForceDisplayOption._Cast_ForceDisplayOption")


__docformat__ = "restructuredtext en"
__all__ = ("ForceDisplayOption",)


class ForceDisplayOption(Enum):
    """ForceDisplayOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FORCE_DISPLAY_OPTION

    INDIVIDUAL = 0
    ALL = 1
    SUM = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ForceDisplayOption.__setattr__ = __enum_setattr
ForceDisplayOption.__delattr__ = __enum_delattr
