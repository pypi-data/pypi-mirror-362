"""ToothTaperSpecification"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TOOTH_TAPER_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "ToothTaperSpecification"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ToothTaperSpecification")
    CastSelf = TypeVar(
        "CastSelf", bound="ToothTaperSpecification._Cast_ToothTaperSpecification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothTaperSpecification",)


class ToothTaperSpecification(Enum):
    """ToothTaperSpecification

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TOOTH_TAPER_SPECIFICATION

    DEPTH = 0
    ANGLE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ToothTaperSpecification.__setattr__ = __enum_setattr
ToothTaperSpecification.__delattr__ = __enum_delattr
