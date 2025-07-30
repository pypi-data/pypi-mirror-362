"""SystemOptimiserTargets"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SYSTEM_OPTIMISER_TARGETS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "SystemOptimiserTargets",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SystemOptimiserTargets")
    CastSelf = TypeVar(
        "CastSelf", bound="SystemOptimiserTargets._Cast_SystemOptimiserTargets"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SystemOptimiserTargets",)


class SystemOptimiserTargets(Enum):
    """SystemOptimiserTargets

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SYSTEM_OPTIMISER_TARGETS

    MINIMUM_FACE_WIDTH = 0
    MINIMUM_MASS = 1
    MINIMUM_WIDEST_FACE_WIDTH = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SystemOptimiserTargets.__setattr__ = __enum_setattr
SystemOptimiserTargets.__delattr__ = __enum_delattr
