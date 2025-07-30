"""TEExcitationType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TE_EXCITATION_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "TEExcitationType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TEExcitationType")
    CastSelf = TypeVar("CastSelf", bound="TEExcitationType._Cast_TEExcitationType")


__docformat__ = "restructuredtext en"
__all__ = ("TEExcitationType",)


class TEExcitationType(Enum):
    """TEExcitationType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TE_EXCITATION_TYPE

    TRANSMISSION_ERROR = 0
    MISALIGNMENT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TEExcitationType.__setattr__ = __enum_setattr
TEExcitationType.__delattr__ = __enum_delattr
