"""SystemOptimiserGearSetOptimisation"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SYSTEM_OPTIMISER_GEAR_SET_OPTIMISATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "SystemOptimiserGearSetOptimisation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SystemOptimiserGearSetOptimisation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SystemOptimiserGearSetOptimisation._Cast_SystemOptimiserGearSetOptimisation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SystemOptimiserGearSetOptimisation",)


class SystemOptimiserGearSetOptimisation(Enum):
    """SystemOptimiserGearSetOptimisation

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SYSTEM_OPTIMISER_GEAR_SET_OPTIMISATION

    NONE = 0
    NORMAL_30_ITERATIONS_OF_MACRO_GEOMETRY_OPTIMISER = 1
    FULL_150_ITERATIONS_OF_MACRO_GEOMETRY_OPTIMISER = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SystemOptimiserGearSetOptimisation.__setattr__ = __enum_setattr
SystemOptimiserGearSetOptimisation.__delattr__ = __enum_delattr
