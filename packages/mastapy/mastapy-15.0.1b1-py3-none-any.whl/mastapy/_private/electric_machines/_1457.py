"""WireSizeSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_WIRE_SIZE_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "WireSizeSpecificationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WireSizeSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WireSizeSpecificationMethod._Cast_WireSizeSpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WireSizeSpecificationMethod",)


class WireSizeSpecificationMethod(Enum):
    """WireSizeSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _WIRE_SIZE_SPECIFICATION_METHOD

    AWG = 0
    IEC_60228 = 1
    USERSPECIFIED = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


WireSizeSpecificationMethod.__setattr__ = __enum_setattr
WireSizeSpecificationMethod.__delattr__ = __enum_delattr
