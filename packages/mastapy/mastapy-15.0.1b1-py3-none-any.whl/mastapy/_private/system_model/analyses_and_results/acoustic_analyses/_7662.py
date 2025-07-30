"""AcousticPreconditionerType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ACOUSTIC_PRECONDITIONER_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses",
    "AcousticPreconditionerType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AcousticPreconditionerType")
    CastSelf = TypeVar(
        "CastSelf", bound="AcousticPreconditionerType._Cast_AcousticPreconditionerType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AcousticPreconditionerType",)


class AcousticPreconditionerType(Enum):
    """AcousticPreconditionerType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ACOUSTIC_PRECONDITIONER_TYPE

    NONE = 0
    NEAR_FIELD = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AcousticPreconditionerType.__setattr__ = __enum_setattr
AcousticPreconditionerType.__delattr__ = __enum_delattr
