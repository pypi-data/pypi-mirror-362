"""LoadCasesToRun"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LOAD_CASES_TO_RUN = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.VersionComparer", "LoadCasesToRun"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadCasesToRun")
    CastSelf = TypeVar("CastSelf", bound="LoadCasesToRun._Cast_LoadCasesToRun")


__docformat__ = "restructuredtext en"
__all__ = ("LoadCasesToRun",)


class LoadCasesToRun(Enum):
    """LoadCasesToRun

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LOAD_CASES_TO_RUN

    HIGHEST_LOAD_IN_EACH_DESIGN_STATE = 0
    HIGHEST_LOAD = 1
    ALL = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LoadCasesToRun.__setattr__ = __enum_setattr
LoadCasesToRun.__delattr__ = __enum_delattr
