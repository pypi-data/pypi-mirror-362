"""PowerLoadDragTorqueSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_POWER_LOAD_DRAG_TORQUE_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.SystemModel", "PowerLoadDragTorqueSpecificationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PowerLoadDragTorqueSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PowerLoadDragTorqueSpecificationMethod._Cast_PowerLoadDragTorqueSpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoadDragTorqueSpecificationMethod",)


class PowerLoadDragTorqueSpecificationMethod(Enum):
    """PowerLoadDragTorqueSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _POWER_LOAD_DRAG_TORQUE_SPECIFICATION_METHOD

    DRAG_TORQUE_FOR_TIME_AND_SPEED = 0
    SPEED_POLYNOMIAL_COEFFICIENTS = 1
    CALCULATED_LINEAR_RESISTANCE_FOR_STEADY_SPEED = 2
    CALCULATED_QUADRATIC_RESISTANCE_FOR_STEADY_SPEED = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


PowerLoadDragTorqueSpecificationMethod.__setattr__ = __enum_setattr
PowerLoadDragTorqueSpecificationMethod.__delattr__ = __enum_delattr
