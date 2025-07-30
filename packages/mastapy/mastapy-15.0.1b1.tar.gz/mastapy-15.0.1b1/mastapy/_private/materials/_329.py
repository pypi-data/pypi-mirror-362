"""AGMAMaterialGrade"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_AGMA_MATERIAL_GRADE = python_net_import("SMT.MastaAPI.Materials", "AGMAMaterialGrade")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AGMAMaterialGrade")
    CastSelf = TypeVar("CastSelf", bound="AGMAMaterialGrade._Cast_AGMAMaterialGrade")


__docformat__ = "restructuredtext en"
__all__ = ("AGMAMaterialGrade",)


class AGMAMaterialGrade(Enum):
    """AGMAMaterialGrade

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _AGMA_MATERIAL_GRADE

    GRADE_1 = 0
    GRADE_2 = 1
    GRADE_3 = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AGMAMaterialGrade.__setattr__ = __enum_setattr
AGMAMaterialGrade.__delattr__ = __enum_delattr
