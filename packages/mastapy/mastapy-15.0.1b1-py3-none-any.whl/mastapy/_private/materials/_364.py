"""MetalPlasticType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_METAL_PLASTIC_TYPE = python_net_import("SMT.MastaAPI.Materials", "MetalPlasticType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MetalPlasticType")
    CastSelf = TypeVar("CastSelf", bound="MetalPlasticType._Cast_MetalPlasticType")


__docformat__ = "restructuredtext en"
__all__ = ("MetalPlasticType",)


class MetalPlasticType(Enum):
    """MetalPlasticType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _METAL_PLASTIC_TYPE

    PLASTIC = 0
    METAL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MetalPlasticType.__setattr__ = __enum_setattr
MetalPlasticType.__delattr__ = __enum_delattr
