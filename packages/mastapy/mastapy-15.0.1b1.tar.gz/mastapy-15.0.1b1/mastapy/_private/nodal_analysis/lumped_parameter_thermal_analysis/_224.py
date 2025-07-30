"""UserDefinedNodeConstraint"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_USER_DEFINED_NODE_CONSTRAINT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "UserDefinedNodeConstraint",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="UserDefinedNodeConstraint")
    CastSelf = TypeVar(
        "CastSelf", bound="UserDefinedNodeConstraint._Cast_UserDefinedNodeConstraint"
    )


__docformat__ = "restructuredtext en"
__all__ = ("UserDefinedNodeConstraint",)


class UserDefinedNodeConstraint(Enum):
    """UserDefinedNodeConstraint

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _USER_DEFINED_NODE_CONSTRAINT

    UNCONSTRAINED = 0
    FIXED_TEMPERATURE = 1
    APPLIED_POWER_LOSS = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


UserDefinedNodeConstraint.__setattr__ = __enum_setattr
UserDefinedNodeConstraint.__delattr__ = __enum_delattr
