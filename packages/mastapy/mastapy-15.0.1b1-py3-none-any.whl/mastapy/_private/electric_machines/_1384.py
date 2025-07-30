"""DQAxisConvention"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DQ_AXIS_CONVENTION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "DQAxisConvention"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DQAxisConvention")
    CastSelf = TypeVar("CastSelf", bound="DQAxisConvention._Cast_DQAxisConvention")


__docformat__ = "restructuredtext en"
__all__ = ("DQAxisConvention",)


class DQAxisConvention(Enum):
    """DQAxisConvention

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DQ_AXIS_CONVENTION

    PERMANENT_MAGNET = 0
    SYNCHRONOUS_RELUCTANCE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DQAxisConvention.__setattr__ = __enum_setattr
DQAxisConvention.__delattr__ = __enum_delattr
