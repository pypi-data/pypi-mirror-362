"""TransientSolverToleranceInputMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TRANSIENT_SOLVER_TOLERANCE_INPUT_METHOD = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "TransientSolverToleranceInputMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TransientSolverToleranceInputMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TransientSolverToleranceInputMethod._Cast_TransientSolverToleranceInputMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TransientSolverToleranceInputMethod",)


class TransientSolverToleranceInputMethod(Enum):
    """TransientSolverToleranceInputMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TRANSIENT_SOLVER_TOLERANCE_INPUT_METHOD

    SIMPLE = 0
    ADVANCED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TransientSolverToleranceInputMethod.__setattr__ = __enum_setattr
TransientSolverToleranceInputMethod.__delattr__ = __enum_delattr
