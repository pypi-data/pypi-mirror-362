"""BayesianOptimizationResultsStorageOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BAYESIAN_OPTIMIZATION_RESULTS_STORAGE_OPTION = python_net_import(
    "SMT.MastaAPI.MathUtility.BayesianOptimization",
    "BayesianOptimizationResultsStorageOption",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BayesianOptimizationResultsStorageOption")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BayesianOptimizationResultsStorageOption._Cast_BayesianOptimizationResultsStorageOption",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BayesianOptimizationResultsStorageOption",)


class BayesianOptimizationResultsStorageOption(Enum):
    """BayesianOptimizationResultsStorageOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BAYESIAN_OPTIMIZATION_RESULTS_STORAGE_OPTION

    OPTIMAL_MEETING_CONSTRAINTS = 0
    ALL_MEETING_CONSTRAINTS = 1
    ALL = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BayesianOptimizationResultsStorageOption.__setattr__ = __enum_setattr
BayesianOptimizationResultsStorageOption.__delattr__ = __enum_delattr
