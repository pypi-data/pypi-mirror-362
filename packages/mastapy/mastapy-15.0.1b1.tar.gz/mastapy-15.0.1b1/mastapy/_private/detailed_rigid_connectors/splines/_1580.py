"""FitTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FIT_TYPES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "FitTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FitTypes")
    CastSelf = TypeVar("CastSelf", bound="FitTypes._Cast_FitTypes")


__docformat__ = "restructuredtext en"
__all__ = ("FitTypes",)


class FitTypes(Enum):
    """FitTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FIT_TYPES

    SIDE_FIT = 0
    MAJOR_DIAMETER_FIT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FitTypes.__setattr__ = __enum_setattr
FitTypes.__delattr__ = __enum_delattr
