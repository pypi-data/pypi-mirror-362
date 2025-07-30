"""EndWindingLengthSource"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_END_WINDING_LENGTH_SOURCE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "EndWindingLengthSource"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="EndWindingLengthSource")
    CastSelf = TypeVar(
        "CastSelf", bound="EndWindingLengthSource._Cast_EndWindingLengthSource"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EndWindingLengthSource",)


class EndWindingLengthSource(Enum):
    """EndWindingLengthSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _END_WINDING_LENGTH_SOURCE

    STRAIGHT_AND_CURVED_EXTENSIONS = 0
    CURVED_EXTENSION_ONLY = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


EndWindingLengthSource.__setattr__ = __enum_setattr
EndWindingLengthSource.__delattr__ = __enum_delattr
