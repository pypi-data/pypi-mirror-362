"""AcousticWeighting"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ACOUSTIC_WEIGHTING = python_net_import("SMT.MastaAPI.MathUtility", "AcousticWeighting")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AcousticWeighting")
    CastSelf = TypeVar("CastSelf", bound="AcousticWeighting._Cast_AcousticWeighting")


__docformat__ = "restructuredtext en"
__all__ = ("AcousticWeighting",)


class AcousticWeighting(Enum):
    """AcousticWeighting

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ACOUSTIC_WEIGHTING

    NONE = 0
    AWEIGHTING = 1
    BWEIGHTING = 2
    CWEIGHTING = 3
    DWEIGHTING = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AcousticWeighting.__setattr__ = __enum_setattr
AcousticWeighting.__delattr__ = __enum_delattr
