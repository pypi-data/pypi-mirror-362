"""ITDesignation"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_IT_DESIGNATION = python_net_import("SMT.MastaAPI.Bearings.Tolerances", "ITDesignation")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ITDesignation")
    CastSelf = TypeVar("CastSelf", bound="ITDesignation._Cast_ITDesignation")


__docformat__ = "restructuredtext en"
__all__ = ("ITDesignation",)


class ITDesignation(Enum):
    """ITDesignation

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _IT_DESIGNATION

    IT1 = 0
    IT2 = 1
    IT3 = 2
    IT4 = 3
    IT5 = 4
    IT6 = 5
    IT7 = 6
    IT8 = 7
    IT9 = 8
    IT10 = 9
    IT11 = 10
    IT12 = 11
    IT13 = 12
    IT14 = 13


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ITDesignation.__setattr__ = __enum_setattr
ITDesignation.__delattr__ = __enum_delattr
