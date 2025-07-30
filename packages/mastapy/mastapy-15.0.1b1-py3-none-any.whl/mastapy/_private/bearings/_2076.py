"""BearingDampingMatrixOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_DAMPING_MATRIX_OPTION = python_net_import(
    "SMT.MastaAPI.Bearings", "BearingDampingMatrixOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingDampingMatrixOption")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingDampingMatrixOption._Cast_BearingDampingMatrixOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingDampingMatrixOption",)


class BearingDampingMatrixOption(Enum):
    """BearingDampingMatrixOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_DAMPING_MATRIX_OPTION

    NO_DAMPING = 0
    SPECIFY_MATRIX = 1
    SPEED_DEPENDENT = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingDampingMatrixOption.__setattr__ = __enum_setattr
BearingDampingMatrixOption.__delattr__ = __enum_delattr
