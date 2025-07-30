"""SafetyRequirementsAGMA"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SAFETY_REQUIREMENTS_AGMA = python_net_import(
    "SMT.MastaAPI.Gears", "SafetyRequirementsAGMA"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SafetyRequirementsAGMA")
    CastSelf = TypeVar(
        "CastSelf", bound="SafetyRequirementsAGMA._Cast_SafetyRequirementsAGMA"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SafetyRequirementsAGMA",)


class SafetyRequirementsAGMA(Enum):
    """SafetyRequirementsAGMA

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SAFETY_REQUIREMENTS_AGMA

    FEWER_THAN_1_FAILURE_IN_10_000 = 0
    FEWER_THAN_1_FAILURE_IN_1000 = 1
    FEWER_THAN_1_FAILURE_IN_100 = 2
    FEWER_THAN_1_FAILURE_IN_10 = 3
    FEWER_THAN_1_FAILURE_IN_2 = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SafetyRequirementsAGMA.__setattr__ = __enum_setattr
SafetyRequirementsAGMA.__delattr__ = __enum_delattr
