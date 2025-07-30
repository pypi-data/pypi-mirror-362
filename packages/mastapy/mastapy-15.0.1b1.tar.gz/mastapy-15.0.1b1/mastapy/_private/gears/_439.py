"""TESpecificationType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TE_SPECIFICATION_TYPE = python_net_import("SMT.MastaAPI.Gears", "TESpecificationType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TESpecificationType")
    CastSelf = TypeVar(
        "CastSelf", bound="TESpecificationType._Cast_TESpecificationType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TESpecificationType",)


class TESpecificationType(Enum):
    """TESpecificationType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TE_SPECIFICATION_TYPE

    LINEAR = 0
    ANGULAR_WITH_RESPECT_TO_WHEEL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TESpecificationType.__setattr__ = __enum_setattr
TESpecificationType.__delattr__ = __enum_delattr
