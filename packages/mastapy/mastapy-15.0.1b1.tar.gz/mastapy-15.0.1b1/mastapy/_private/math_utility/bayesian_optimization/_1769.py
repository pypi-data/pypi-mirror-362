"""OptimizationStage"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_OPTIMIZATION_STAGE = python_net_import(
    "SMT.MastaAPI.MathUtility.BayesianOptimization", "OptimizationStage"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OptimizationStage")
    CastSelf = TypeVar("CastSelf", bound="OptimizationStage._Cast_OptimizationStage")


__docformat__ = "restructuredtext en"
__all__ = ("OptimizationStage",)


class OptimizationStage(Enum):
    """OptimizationStage

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _OPTIMIZATION_STAGE

    UNKNOWN = 1
    SETUP = 2
    NOT_STARTED = 4
    INITIAL_SAMPLING = 8
    INITIAL_SAMPLING_COMPLETE_RUN_TO_OPTIMISE = 16
    ERROR_DURING_INITIAL_SAMPLING = 32
    INITIAL_SAMPLING_FAILED = 64
    OPTIMIZING = 128
    ERROR_DURING_OPTIMIZATION = 256
    ERROR_OCCURRED = 352
    SAMPLING_COMPLETED_SUCCESSFULLY = 400
    SEARCHING_FOR_CANDIDATES_THAT_MEET_CONSTRAINTS = 512
    INITIAL_SAMPLING_COMPLETE_RUN_TO_FIND_CANDIDATES_THAT_SATISFY_THE_CONSTRAINTS = 1024


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


OptimizationStage.__setattr__ = __enum_setattr
OptimizationStage.__delattr__ = __enum_delattr
