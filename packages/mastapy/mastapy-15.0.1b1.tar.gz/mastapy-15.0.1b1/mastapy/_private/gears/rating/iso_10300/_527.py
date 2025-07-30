"""ProfileCrowningSetting"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PROFILE_CROWNING_SETTING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ProfileCrowningSetting"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ProfileCrowningSetting")
    CastSelf = TypeVar(
        "CastSelf", bound="ProfileCrowningSetting._Cast_ProfileCrowningSetting"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ProfileCrowningSetting",)


class ProfileCrowningSetting(Enum):
    """ProfileCrowningSetting

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PROFILE_CROWNING_SETTING

    PROFILE_CROWNING_LOW_AUTOMOTIVE_GEARS = 0
    PROFILE_CROWNING_HIGH_INDUSTRIAL_GEARS = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ProfileCrowningSetting.__setattr__ = __enum_setattr
ProfileCrowningSetting.__delattr__ = __enum_delattr
