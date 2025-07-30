"""InputVelocityForRunUpProcessingType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_INPUT_VELOCITY_FOR_RUN_UP_PROCESSING_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "InputVelocityForRunUpProcessingType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InputVelocityForRunUpProcessingType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InputVelocityForRunUpProcessingType._Cast_InputVelocityForRunUpProcessingType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InputVelocityForRunUpProcessingType",)


class InputVelocityForRunUpProcessingType(Enum):
    """InputVelocityForRunUpProcessingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _INPUT_VELOCITY_FOR_RUN_UP_PROCESSING_TYPE

    NONE = 0
    FIT_POLYNOMIAL = 1
    FILTER = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


InputVelocityForRunUpProcessingType.__setattr__ = __enum_setattr
InputVelocityForRunUpProcessingType.__delattr__ = __enum_delattr
