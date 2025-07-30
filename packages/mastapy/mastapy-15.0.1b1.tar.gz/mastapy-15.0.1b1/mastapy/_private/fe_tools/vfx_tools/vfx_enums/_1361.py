"""ProSolveMpcType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PRO_SOLVE_MPC_TYPE = python_net_import(
    "SMT.MastaAPI.FETools.VfxTools.VfxEnums", "ProSolveMpcType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ProSolveMpcType")
    CastSelf = TypeVar("CastSelf", bound="ProSolveMpcType._Cast_ProSolveMpcType")


__docformat__ = "restructuredtext en"
__all__ = ("ProSolveMpcType",)


class ProSolveMpcType(Enum):
    """ProSolveMpcType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PRO_SOLVE_MPC_TYPE

    PENALTY_FUNCTION_METHOD = 1
    LAGRANGE_MULTIPLIER_METHOD = 2
    AUGMENTED_LAGRANGE_MULTIPLIER_METHOD = 3
    MATRIX_TRANSFORMATION_METHOD = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ProSolveMpcType.__setattr__ = __enum_setattr
ProSolveMpcType.__delattr__ = __enum_delattr
