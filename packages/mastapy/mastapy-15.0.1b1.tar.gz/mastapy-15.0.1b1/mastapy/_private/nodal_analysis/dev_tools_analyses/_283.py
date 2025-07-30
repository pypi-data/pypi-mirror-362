"""MassMatrixType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MASS_MATRIX_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "MassMatrixType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MassMatrixType")
    CastSelf = TypeVar("CastSelf", bound="MassMatrixType._Cast_MassMatrixType")


__docformat__ = "restructuredtext en"
__all__ = ("MassMatrixType",)


class MassMatrixType(Enum):
    """MassMatrixType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MASS_MATRIX_TYPE

    DIAGONAL = 0
    CONSISTENT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MassMatrixType.__setattr__ = __enum_setattr
MassMatrixType.__delattr__ = __enum_delattr
