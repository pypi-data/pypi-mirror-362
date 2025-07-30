"""ModelSplittingMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MODEL_SPLITTING_METHOD = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "ModelSplittingMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ModelSplittingMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="ModelSplittingMethod._Cast_ModelSplittingMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModelSplittingMethod",)


class ModelSplittingMethod(Enum):
    """ModelSplittingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MODEL_SPLITTING_METHOD

    NONE = 0
    ELEMENT_PROPERTY_ID = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ModelSplittingMethod.__setattr__ = __enum_setattr
ModelSplittingMethod.__delattr__ = __enum_delattr
