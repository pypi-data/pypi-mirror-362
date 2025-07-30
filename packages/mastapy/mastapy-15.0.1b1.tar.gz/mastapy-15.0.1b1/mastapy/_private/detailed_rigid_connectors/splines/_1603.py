"""SplineToleranceClassTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SPLINE_TOLERANCE_CLASS_TYPES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "SplineToleranceClassTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SplineToleranceClassTypes")
    CastSelf = TypeVar(
        "CastSelf", bound="SplineToleranceClassTypes._Cast_SplineToleranceClassTypes"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SplineToleranceClassTypes",)


class SplineToleranceClassTypes(Enum):
    """SplineToleranceClassTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SPLINE_TOLERANCE_CLASS_TYPES

    _4 = 0
    _5 = 1
    _6 = 2
    _7 = 3
    _8 = 4
    _9 = 5
    _10 = 6
    _11 = 7
    _12 = 8


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SplineToleranceClassTypes.__setattr__ = __enum_setattr
SplineToleranceClassTypes.__delattr__ = __enum_delattr
