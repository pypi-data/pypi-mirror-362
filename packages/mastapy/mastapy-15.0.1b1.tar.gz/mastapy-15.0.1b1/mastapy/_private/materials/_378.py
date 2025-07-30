"""VDI2736LubricantType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_VDI2736_LUBRICANT_TYPE = python_net_import(
    "SMT.MastaAPI.Materials", "VDI2736LubricantType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="VDI2736LubricantType")
    CastSelf = TypeVar(
        "CastSelf", bound="VDI2736LubricantType._Cast_VDI2736LubricantType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("VDI2736LubricantType",)


class VDI2736LubricantType(Enum):
    """VDI2736LubricantType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _VDI2736_LUBRICANT_TYPE

    OIL = 0
    GREASE = 1
    WATEROIL_EMULSION = 2
    OIL_MIST = 3
    NONE_DRY_RUNNING = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


VDI2736LubricantType.__setattr__ = __enum_setattr
VDI2736LubricantType.__delattr__ = __enum_delattr
