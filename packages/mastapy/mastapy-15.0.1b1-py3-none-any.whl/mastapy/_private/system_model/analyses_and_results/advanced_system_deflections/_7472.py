"""UseLtcaInAsdOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_USE_LTCA_IN_ASD_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "UseLtcaInAsdOption",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="UseLtcaInAsdOption")
    CastSelf = TypeVar("CastSelf", bound="UseLtcaInAsdOption._Cast_UseLtcaInAsdOption")


__docformat__ = "restructuredtext en"
__all__ = ("UseLtcaInAsdOption",)


class UseLtcaInAsdOption(Enum):
    """UseLtcaInAsdOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _USE_LTCA_IN_ASD_OPTION

    NO = 0
    YES = 1
    AUTO = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


UseLtcaInAsdOption.__setattr__ = __enum_setattr
UseLtcaInAsdOption.__delattr__ = __enum_delattr
