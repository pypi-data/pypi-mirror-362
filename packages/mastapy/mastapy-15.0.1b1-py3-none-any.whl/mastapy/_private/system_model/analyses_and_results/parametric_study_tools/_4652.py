"""ParametricStudyDimension"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PARAMETRIC_STUDY_DIMENSION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyDimension",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ParametricStudyDimension")
    CastSelf = TypeVar(
        "CastSelf", bound="ParametricStudyDimension._Cast_ParametricStudyDimension"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyDimension",)


class ParametricStudyDimension(Enum):
    """ParametricStudyDimension

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PARAMETRIC_STUDY_DIMENSION

    DIMENSION_1 = 1
    DIMENSION_2 = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ParametricStudyDimension.__setattr__ = __enum_setattr
ParametricStudyDimension.__delattr__ = __enum_delattr
