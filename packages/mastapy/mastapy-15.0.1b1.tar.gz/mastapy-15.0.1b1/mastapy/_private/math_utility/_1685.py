"""CoordinateSystemForRotation"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COORDINATE_SYSTEM_FOR_ROTATION = python_net_import(
    "SMT.MastaAPI.MathUtility", "CoordinateSystemForRotation"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CoordinateSystemForRotation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoordinateSystemForRotation._Cast_CoordinateSystemForRotation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoordinateSystemForRotation",)


class CoordinateSystemForRotation(Enum):
    """CoordinateSystemForRotation

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COORDINATE_SYSTEM_FOR_ROTATION

    WORLD_COORDINATE_SYSTEM = 0
    LOCAL_COORDINATE_SYSTEM = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CoordinateSystemForRotation.__setattr__ = __enum_setattr
CoordinateSystemForRotation.__delattr__ = __enum_delattr
