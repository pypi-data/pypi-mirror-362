"""CoordinateSystemForRotationOrigin"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COORDINATE_SYSTEM_FOR_ROTATION_ORIGIN = python_net_import(
    "SMT.MastaAPI.MathUtility", "CoordinateSystemForRotationOrigin"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CoordinateSystemForRotationOrigin")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoordinateSystemForRotationOrigin._Cast_CoordinateSystemForRotationOrigin",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoordinateSystemForRotationOrigin",)


class CoordinateSystemForRotationOrigin(Enum):
    """CoordinateSystemForRotationOrigin

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COORDINATE_SYSTEM_FOR_ROTATION_ORIGIN

    WORLD_COORDINATE_SYSTEM = 0
    LOCAL_COORDINATE_SYSTEM = 1
    USERSPECIFIED = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CoordinateSystemForRotationOrigin.__setattr__ = __enum_setattr
CoordinateSystemForRotationOrigin.__delattr__ = __enum_delattr
