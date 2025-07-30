"""GravityForceSource"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GRAVITY_FORCE_SOURCE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "GravityForceSource"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GravityForceSource")
    CastSelf = TypeVar("CastSelf", bound="GravityForceSource._Cast_GravityForceSource")


__docformat__ = "restructuredtext en"
__all__ = ("GravityForceSource",)


class GravityForceSource(Enum):
    """GravityForceSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GRAVITY_FORCE_SOURCE

    NOT_AVAILABLE = 0
    CALCULATED_FROM_MASS_MATRIX = 1
    CALCULATED_FROM_X_Y_Z_COMPONENTS = 2
    IMPORTED_SINGLE_VECTOR = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GravityForceSource.__setattr__ = __enum_setattr
GravityForceSource.__delattr__ = __enum_delattr
