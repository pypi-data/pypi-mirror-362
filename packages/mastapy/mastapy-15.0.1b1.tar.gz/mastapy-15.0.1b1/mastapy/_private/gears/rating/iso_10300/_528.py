"""VerificationOfContactPattern"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_VERIFICATION_OF_CONTACT_PATTERN = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "VerificationOfContactPattern"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="VerificationOfContactPattern")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VerificationOfContactPattern._Cast_VerificationOfContactPattern",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VerificationOfContactPattern",)


class VerificationOfContactPattern(Enum):
    """VerificationOfContactPattern

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _VERIFICATION_OF_CONTACT_PATTERN

    FOR_EACH_GEAR_SET_IN_ITS_HOUSING_UNDER_FULL_LOAD = 0
    FOR_EACH_GEAR_SET_UNDER_LIGHT_TEST_LOAD = 1
    FOR_A_SAMPLE_GEAR_SET_AND_ESTIMATED_FOR_FULL_LOAD = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


VerificationOfContactPattern.__setattr__ = __enum_setattr
VerificationOfContactPattern.__delattr__ = __enum_delattr
