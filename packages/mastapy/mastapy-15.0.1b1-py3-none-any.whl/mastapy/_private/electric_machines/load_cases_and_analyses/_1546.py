"""EndWindingInductanceMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_END_WINDING_INDUCTANCE_METHOD = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "EndWindingInductanceMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="EndWindingInductanceMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="EndWindingInductanceMethod._Cast_EndWindingInductanceMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EndWindingInductanceMethod",)


class EndWindingInductanceMethod(Enum):
    """EndWindingInductanceMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _END_WINDING_INDUCTANCE_METHOD

    NONE = 0
    ROSA_AND_GROVER = 1
    USERSPECIFIED = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


EndWindingInductanceMethod.__setattr__ = __enum_setattr
EndWindingInductanceMethod.__delattr__ = __enum_delattr
