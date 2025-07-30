"""MechanicalSolverType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MECHANICAL_SOLVER_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.Elmer", "MechanicalSolverType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MechanicalSolverType")
    CastSelf = TypeVar(
        "CastSelf", bound="MechanicalSolverType._Cast_MechanicalSolverType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MechanicalSolverType",)


class MechanicalSolverType(Enum):
    """MechanicalSolverType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MECHANICAL_SOLVER_TYPE

    DIRECT = 0
    ITERATIVE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MechanicalSolverType.__setattr__ = __enum_setattr
MechanicalSolverType.__delattr__ = __enum_delattr
