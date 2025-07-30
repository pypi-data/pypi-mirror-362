"""InnerDiameterReference"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_INNER_DIAMETER_REFERENCE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "InnerDiameterReference"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InnerDiameterReference")
    CastSelf = TypeVar(
        "CastSelf", bound="InnerDiameterReference._Cast_InnerDiameterReference"
    )


__docformat__ = "restructuredtext en"
__all__ = ("InnerDiameterReference",)


class InnerDiameterReference(Enum):
    """InnerDiameterReference

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _INNER_DIAMETER_REFERENCE

    FLUX = 0
    MASTA = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


InnerDiameterReference.__setattr__ = __enum_setattr
InnerDiameterReference.__delattr__ = __enum_delattr
