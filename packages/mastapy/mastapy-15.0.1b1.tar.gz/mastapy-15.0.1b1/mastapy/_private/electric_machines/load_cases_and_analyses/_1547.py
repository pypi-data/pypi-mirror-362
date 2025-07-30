"""LeadingOrLagging"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LEADING_OR_LAGGING = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "LeadingOrLagging"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LeadingOrLagging")
    CastSelf = TypeVar("CastSelf", bound="LeadingOrLagging._Cast_LeadingOrLagging")


__docformat__ = "restructuredtext en"
__all__ = ("LeadingOrLagging",)


class LeadingOrLagging(Enum):
    """LeadingOrLagging

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LEADING_OR_LAGGING

    LEADING = 0
    LAGGING = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LeadingOrLagging.__setattr__ = __enum_setattr
LeadingOrLagging.__delattr__ = __enum_delattr
