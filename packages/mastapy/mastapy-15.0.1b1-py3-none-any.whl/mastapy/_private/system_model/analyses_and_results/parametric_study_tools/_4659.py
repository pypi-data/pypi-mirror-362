"""ParametricStudyToolStepSaveMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PARAMETRIC_STUDY_TOOL_STEP_SAVE_METHOD = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyToolStepSaveMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ParametricStudyToolStepSaveMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ParametricStudyToolStepSaveMethod._Cast_ParametricStudyToolStepSaveMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyToolStepSaveMethod",)


class ParametricStudyToolStepSaveMethod(Enum):
    """ParametricStudyToolStepSaveMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PARAMETRIC_STUDY_TOOL_STEP_SAVE_METHOD

    INDIVIDUAL_FILES = 0
    SINGLE_FILE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ParametricStudyToolStepSaveMethod.__setattr__ = __enum_setattr
ParametricStudyToolStepSaveMethod.__delattr__ = __enum_delattr
