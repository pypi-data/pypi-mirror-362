"""HypoidWindUpRemovalMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HYPOID_WIND_UP_REMOVAL_METHOD = python_net_import(
    "SMT.MastaAPI.SystemModel", "HypoidWindUpRemovalMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HypoidWindUpRemovalMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="HypoidWindUpRemovalMethod._Cast_HypoidWindUpRemovalMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidWindUpRemovalMethod",)


class HypoidWindUpRemovalMethod(Enum):
    """HypoidWindUpRemovalMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HYPOID_WIND_UP_REMOVAL_METHOD

    INVARIANT_UNDER_RIGID_BODY_TRANSLATIONS_AND_ROTATIONS = 0
    ZERO_WIND_UP_SAE_750152 = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HypoidWindUpRemovalMethod.__setattr__ = __enum_setattr
HypoidWindUpRemovalMethod.__delattr__ = __enum_delattr
