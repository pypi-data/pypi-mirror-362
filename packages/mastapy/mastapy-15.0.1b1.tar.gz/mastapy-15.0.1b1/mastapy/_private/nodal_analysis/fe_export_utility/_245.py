"""BoundaryConditionType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BOUNDARY_CONDITION_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.FeExportUtility", "BoundaryConditionType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BoundaryConditionType")
    CastSelf = TypeVar(
        "CastSelf", bound="BoundaryConditionType._Cast_BoundaryConditionType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BoundaryConditionType",)


class BoundaryConditionType(Enum):
    """BoundaryConditionType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BOUNDARY_CONDITION_TYPE

    FORCE = 0
    DISPLACEMENT = 1
    NONE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BoundaryConditionType.__setattr__ = __enum_setattr
BoundaryConditionType.__delattr__ = __enum_delattr
