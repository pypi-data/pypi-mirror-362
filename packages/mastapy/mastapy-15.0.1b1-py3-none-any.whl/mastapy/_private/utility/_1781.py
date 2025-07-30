"""LoadCaseOverrideOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LOAD_CASE_OVERRIDE_OPTION = python_net_import(
    "SMT.MastaAPI.Utility", "LoadCaseOverrideOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadCaseOverrideOption")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadCaseOverrideOption._Cast_LoadCaseOverrideOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadCaseOverrideOption",)


class LoadCaseOverrideOption(Enum):
    """LoadCaseOverrideOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LOAD_CASE_OVERRIDE_OPTION

    LOAD_CASE_SETTING = 0
    YES = 1
    NO = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LoadCaseOverrideOption.__setattr__ = __enum_setattr
LoadCaseOverrideOption.__delattr__ = __enum_delattr
