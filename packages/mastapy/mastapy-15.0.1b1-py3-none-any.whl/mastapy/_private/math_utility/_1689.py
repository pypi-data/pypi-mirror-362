"""DynamicsResponseScalarResult"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DYNAMICS_RESPONSE_SCALAR_RESULT = python_net_import(
    "SMT.MastaAPI.MathUtility", "DynamicsResponseScalarResult"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DynamicsResponseScalarResult")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DynamicsResponseScalarResult._Cast_DynamicsResponseScalarResult",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicsResponseScalarResult",)


class DynamicsResponseScalarResult(Enum):
    """DynamicsResponseScalarResult

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DYNAMICS_RESPONSE_SCALAR_RESULT

    X = 0
    Y = 1
    Z = 2
    ΘX = 3
    ΘY = 4
    ΘZ = 5
    MAGNITUDE_XYZ = 6
    MAGNITUDE_XY = 7
    MAGNITUDE_ΘXΘYΘZ = 8
    MAGNITUDE_ΘX_ΘY = 9


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DynamicsResponseScalarResult.__setattr__ = __enum_setattr
DynamicsResponseScalarResult.__delattr__ = __enum_delattr
