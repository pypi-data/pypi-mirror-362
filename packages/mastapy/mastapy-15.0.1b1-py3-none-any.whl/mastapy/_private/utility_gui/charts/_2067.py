"""SMTAxis"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SMT_AXIS = python_net_import("SMT.MastaAPI.UtilityGUI.Charts", "SMTAxis")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SMTAxis")
    CastSelf = TypeVar("CastSelf", bound="SMTAxis._Cast_SMTAxis")


__docformat__ = "restructuredtext en"
__all__ = ("SMTAxis",)


class SMTAxis(Enum):
    """SMTAxis

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SMT_AXIS

    PRIMARYX = 0
    SECONDARYX = 1
    TERTIARYX = 2
    PRIMARYY = 3
    SECONDARYY = 4
    DEPTH = 5
    POLAR = 6
    POLARANGLE = 7
    I_ = 8
    J = 9
    RESULT = 10


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SMTAxis.__setattr__ = __enum_setattr
SMTAxis.__delattr__ = __enum_delattr
