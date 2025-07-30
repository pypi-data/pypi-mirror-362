"""ResultOptionsFor3DVector"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RESULT_OPTIONS_FOR_3D_VECTOR = python_net_import(
    "SMT.MastaAPI.MathUtility", "ResultOptionsFor3DVector"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ResultOptionsFor3DVector")
    CastSelf = TypeVar(
        "CastSelf", bound="ResultOptionsFor3DVector._Cast_ResultOptionsFor3DVector"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultOptionsFor3DVector",)


class ResultOptionsFor3DVector(Enum):
    """ResultOptionsFor3DVector

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RESULT_OPTIONS_FOR_3D_VECTOR

    X = 0
    Y = 1
    Z = 2
    MAGNITUDE_XY = 3
    MAGNITUDE = 4
    RADIAL_XY = 5
    TANGENTIAL_XY = 6


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ResultOptionsFor3DVector.__setattr__ = __enum_setattr
ResultOptionsFor3DVector.__delattr__ = __enum_delattr
