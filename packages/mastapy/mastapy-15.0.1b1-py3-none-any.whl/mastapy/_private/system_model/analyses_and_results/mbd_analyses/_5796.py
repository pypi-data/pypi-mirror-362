"""TorqueConverterLockupRule"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TORQUE_CONVERTER_LOCKUP_RULE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "TorqueConverterLockupRule",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TorqueConverterLockupRule")
    CastSelf = TypeVar(
        "CastSelf", bound="TorqueConverterLockupRule._Cast_TorqueConverterLockupRule"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterLockupRule",)


class TorqueConverterLockupRule(Enum):
    """TorqueConverterLockupRule

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TORQUE_CONVERTER_LOCKUP_RULE

    SPECIFY_TIME = 0
    SPEED_RATIO_AND_VEHICLE_SPEED = 1
    PRESSURE_VS_TIME = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TorqueConverterLockupRule.__setattr__ = __enum_setattr
TorqueConverterLockupRule.__delattr__ = __enum_delattr
