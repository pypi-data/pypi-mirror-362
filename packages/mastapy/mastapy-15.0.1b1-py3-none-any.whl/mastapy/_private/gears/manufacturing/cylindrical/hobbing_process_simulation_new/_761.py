"""ActiveProcessMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ACTIVE_PROCESS_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "ActiveProcessMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ActiveProcessMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="ActiveProcessMethod._Cast_ActiveProcessMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ActiveProcessMethod",)


class ActiveProcessMethod(Enum):
    """ActiveProcessMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ACTIVE_PROCESS_METHOD

    ROUGH_PROCESS_SIMULATION = 0
    FINISH_PROCESS_SIMULATION = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ActiveProcessMethod.__setattr__ = __enum_setattr
ActiveProcessMethod.__delattr__ = __enum_delattr
