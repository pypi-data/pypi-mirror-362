"""CylinderOrientation"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CYLINDER_ORIENTATION = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis", "CylinderOrientation"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylinderOrientation")
    CastSelf = TypeVar(
        "CastSelf", bound="CylinderOrientation._Cast_CylinderOrientation"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylinderOrientation",)


class CylinderOrientation(Enum):
    """CylinderOrientation

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CYLINDER_ORIENTATION

    HORIZONTAL = 0
    VERTICAL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CylinderOrientation.__setattr__ = __enum_setattr
CylinderOrientation.__delattr__ = __enum_delattr
