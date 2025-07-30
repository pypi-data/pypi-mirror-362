"""ProfileToFit"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PROFILE_TO_FIT = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles", "ProfileToFit"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ProfileToFit")
    CastSelf = TypeVar("CastSelf", bound="ProfileToFit._Cast_ProfileToFit")


__docformat__ = "restructuredtext en"
__all__ = ("ProfileToFit",)


class ProfileToFit(Enum):
    """ProfileToFit

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PROFILE_TO_FIT

    AUTO = 0
    QUADRATIC = 1
    DIN_LUNDBERG = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ProfileToFit.__setattr__ = __enum_setattr
ProfileToFit.__delattr__ = __enum_delattr
