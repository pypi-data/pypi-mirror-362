"""ComponentOrientationOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COMPONENT_ORIENTATION_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "ComponentOrientationOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ComponentOrientationOption")
    CastSelf = TypeVar(
        "CastSelf", bound="ComponentOrientationOption._Cast_ComponentOrientationOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentOrientationOption",)


class ComponentOrientationOption(Enum):
    """ComponentOrientationOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COMPONENT_ORIENTATION_OPTION

    DO_NOT_CHANGE = 0
    ALIGN_WITH_FE_AXES = 1
    ALIGN_NORMAL_TO_FE_SURFACE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ComponentOrientationOption.__setattr__ = __enum_setattr
ComponentOrientationOption.__delattr__ = __enum_delattr
