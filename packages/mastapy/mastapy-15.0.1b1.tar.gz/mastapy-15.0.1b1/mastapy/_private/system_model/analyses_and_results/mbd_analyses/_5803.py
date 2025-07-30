"""WheelSlipType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_WHEEL_SLIP_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses", "WheelSlipType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WheelSlipType")
    CastSelf = TypeVar("CastSelf", bound="WheelSlipType._Cast_WheelSlipType")


__docformat__ = "restructuredtext en"
__all__ = ("WheelSlipType",)


class WheelSlipType(Enum):
    """WheelSlipType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _WHEEL_SLIP_TYPE

    NO_SLIP = 0
    BASIC_SLIP = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


WheelSlipType.__setattr__ = __enum_setattr
WheelSlipType.__delattr__ = __enum_delattr
