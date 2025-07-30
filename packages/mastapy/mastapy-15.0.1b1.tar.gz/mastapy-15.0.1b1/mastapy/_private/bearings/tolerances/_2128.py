"""TypeOfFit"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TYPE_OF_FIT = python_net_import("SMT.MastaAPI.Bearings.Tolerances", "TypeOfFit")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TypeOfFit")
    CastSelf = TypeVar("CastSelf", bound="TypeOfFit._Cast_TypeOfFit")


__docformat__ = "restructuredtext en"
__all__ = ("TypeOfFit",)


class TypeOfFit(Enum):
    """TypeOfFit

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TYPE_OF_FIT

    SPLINE = 0
    LINEAR = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TypeOfFit.__setattr__ = __enum_setattr
TypeOfFit.__delattr__ = __enum_delattr
