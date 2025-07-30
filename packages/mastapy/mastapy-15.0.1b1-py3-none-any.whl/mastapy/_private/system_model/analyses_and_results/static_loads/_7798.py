"""ParametricStudyType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PARAMETRIC_STUDY_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ParametricStudyType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ParametricStudyType")
    CastSelf = TypeVar(
        "CastSelf", bound="ParametricStudyType._Cast_ParametricStudyType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyType",)


class ParametricStudyType(Enum):
    """ParametricStudyType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PARAMETRIC_STUDY_TYPE

    LINEAR_SWEEP = 0
    MONTE_CARLO = 1
    LATIN_HYPERCUBE = 2
    DESIGN_OF_EXPERIMENTS = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ParametricStudyType.__setattr__ = __enum_setattr
ParametricStudyType.__delattr__ = __enum_delattr
