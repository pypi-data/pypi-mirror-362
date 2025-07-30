"""QualityGrade"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_QUALITY_GRADE = python_net_import("SMT.MastaAPI.Materials", "QualityGrade")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="QualityGrade")
    CastSelf = TypeVar("CastSelf", bound="QualityGrade._Cast_QualityGrade")


__docformat__ = "restructuredtext en"
__all__ = ("QualityGrade",)


class QualityGrade(Enum):
    """QualityGrade

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _QUALITY_GRADE

    ML = 0
    MQ = 1
    ME = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


QualityGrade.__setattr__ = __enum_setattr
QualityGrade.__delattr__ = __enum_delattr
