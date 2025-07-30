"""ContactRatioDataSource"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CONTACT_RATIO_DATA_SOURCE = python_net_import(
    "SMT.MastaAPI.Gears", "ContactRatioDataSource"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ContactRatioDataSource")
    CastSelf = TypeVar(
        "CastSelf", bound="ContactRatioDataSource._Cast_ContactRatioDataSource"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ContactRatioDataSource",)


class ContactRatioDataSource(Enum):
    """ContactRatioDataSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CONTACT_RATIO_DATA_SOURCE

    DESIGN = 0
    OPERATING = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ContactRatioDataSource.__setattr__ = __enum_setattr
ContactRatioDataSource.__delattr__ = __enum_delattr
