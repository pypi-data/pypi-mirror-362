"""CouplingType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COUPLING_TYPE = python_net_import("SMT.MastaAPI.NodalAnalysis", "CouplingType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CouplingType")
    CastSelf = TypeVar("CastSelf", bound="CouplingType._Cast_CouplingType")


__docformat__ = "restructuredtext en"
__all__ = ("CouplingType",)


class CouplingType(Enum):
    """CouplingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COUPLING_TYPE

    DISPLACEMENT = 0
    VELOCITY = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CouplingType.__setattr__ = __enum_setattr
CouplingType.__delattr__ = __enum_delattr
