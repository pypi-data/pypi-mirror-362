"""TransientSolverStatus"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TRANSIENT_SOLVER_STATUS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "TransientSolverStatus"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TransientSolverStatus")
    CastSelf = TypeVar(
        "CastSelf", bound="TransientSolverStatus._Cast_TransientSolverStatus"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TransientSolverStatus",)


class TransientSolverStatus(Enum):
    """TransientSolverStatus

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TRANSIENT_SOLVER_STATUS

    NONE = 0
    PREPARED_FOR_ANALYSIS = 1
    ANALYSIS_RUNNING = 2
    END_TIME_REACHED = 3
    MAXIMUM_TIME_STEPS_REACHED = 4
    ANALYSIS_ABORTED = 5
    ERROR_OCCURRED = 6
    END_MINOR_STEP_REACHED = 7
    FAILED_DUE_TO_MAXIMUM_NUMBER_OF_FAILED_STEPS_AT_MINIMUM_STEP = 8


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TransientSolverStatus.__setattr__ = __enum_setattr
TransientSolverStatus.__delattr__ = __enum_delattr
