"""DestinationDesignState"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DESTINATION_DESIGN_STATE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "DestinationDesignState",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DestinationDesignState")
    CastSelf = TypeVar(
        "CastSelf", bound="DestinationDesignState._Cast_DestinationDesignState"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DestinationDesignState",)


class DestinationDesignState(Enum):
    """DestinationDesignState

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DESTINATION_DESIGN_STATE

    NAMES = 0
    GEAR_RATIO = 1
    NONE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DestinationDesignState.__setattr__ = __enum_setattr
DestinationDesignState.__delattr__ = __enum_delattr
