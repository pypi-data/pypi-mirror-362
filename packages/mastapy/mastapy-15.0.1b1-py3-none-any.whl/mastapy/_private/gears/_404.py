"""AGMAToleranceStandard"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_AGMA_TOLERANCE_STANDARD = python_net_import(
    "SMT.MastaAPI.Gears", "AGMAToleranceStandard"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AGMAToleranceStandard")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMAToleranceStandard._Cast_AGMAToleranceStandard"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAToleranceStandard",)


class AGMAToleranceStandard(Enum):
    """AGMAToleranceStandard

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _AGMA_TOLERANCE_STANDARD

    AGMA_20151A01 = 0
    AGMA_2000A88 = 1
    ANSIAGMA_ISO_13281B14 = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AGMAToleranceStandard.__setattr__ = __enum_setattr
AGMAToleranceStandard.__delattr__ = __enum_delattr
