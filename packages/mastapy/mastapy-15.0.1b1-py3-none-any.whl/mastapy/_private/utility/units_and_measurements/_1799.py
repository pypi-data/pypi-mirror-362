"""MeasurementSystem"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MEASUREMENT_SYSTEM = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements", "MeasurementSystem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MeasurementSystem")
    CastSelf = TypeVar("CastSelf", bound="MeasurementSystem._Cast_MeasurementSystem")


__docformat__ = "restructuredtext en"
__all__ = ("MeasurementSystem",)


class MeasurementSystem(Enum):
    """MeasurementSystem

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MEASUREMENT_SYSTEM

    METRIC = 0
    IMPERIAL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MeasurementSystem.__setattr__ = __enum_setattr
MeasurementSystem.__delattr__ = __enum_delattr
