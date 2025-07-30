"""TorqueValuesObtainedFrom"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TORQUE_VALUES_OBTAINED_FROM = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "TorqueValuesObtainedFrom",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TorqueValuesObtainedFrom")
    CastSelf = TypeVar(
        "CastSelf", bound="TorqueValuesObtainedFrom._Cast_TorqueValuesObtainedFrom"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueValuesObtainedFrom",)


class TorqueValuesObtainedFrom(Enum):
    """TorqueValuesObtainedFrom

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TORQUE_VALUES_OBTAINED_FROM

    BIN_CENTRES = 0
    LARGEST_MAGNITUDE = 1
    AVERAGE_OF_BIN_CONTENTS = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TorqueValuesObtainedFrom.__setattr__ = __enum_setattr
TorqueValuesObtainedFrom.__delattr__ = __enum_delattr
