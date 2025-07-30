"""ISOToleranceStandard"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ISO_TOLERANCE_STANDARD = python_net_import(
    "SMT.MastaAPI.Gears", "ISOToleranceStandard"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ISOToleranceStandard")
    CastSelf = TypeVar(
        "CastSelf", bound="ISOToleranceStandard._Cast_ISOToleranceStandard"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISOToleranceStandard",)


class ISOToleranceStandard(Enum):
    """ISOToleranceStandard

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ISO_TOLERANCE_STANDARD

    ISO_132811995EISO_132821997E = 0
    ISO_132812013EISO_132821997E = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ISOToleranceStandard.__setattr__ = __enum_setattr
ISOToleranceStandard.__delattr__ = __enum_delattr
