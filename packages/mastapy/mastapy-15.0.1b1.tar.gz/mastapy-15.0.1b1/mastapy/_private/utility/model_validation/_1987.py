"""Severity"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SEVERITY = python_net_import("SMT.MastaAPI.Utility.ModelValidation", "Severity")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Severity")
    CastSelf = TypeVar("CastSelf", bound="Severity._Cast_Severity")


__docformat__ = "restructuredtext en"
__all__ = ("Severity",)


class Severity(Enum):
    """Severity

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SEVERITY

    INFORMATION = 1
    WARNING = 2
    ERROR = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


Severity.__setattr__ = __enum_setattr
Severity.__delattr__ = __enum_delattr
