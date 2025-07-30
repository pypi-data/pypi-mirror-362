"""SNCurveDefinition"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SN_CURVE_DEFINITION = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "SNCurveDefinition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SNCurveDefinition")
    CastSelf = TypeVar("CastSelf", bound="SNCurveDefinition._Cast_SNCurveDefinition")


__docformat__ = "restructuredtext en"
__all__ = ("SNCurveDefinition",)


class SNCurveDefinition(Enum):
    """SNCurveDefinition

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SN_CURVE_DEFINITION

    AGMA = 0
    GLEASON = 1
    CUSTOM = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SNCurveDefinition.__setattr__ = __enum_setattr
SNCurveDefinition.__delattr__ = __enum_delattr
