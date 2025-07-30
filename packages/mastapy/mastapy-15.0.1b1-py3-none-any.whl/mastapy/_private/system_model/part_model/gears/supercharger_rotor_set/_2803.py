"""YVariableForImportedData"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_Y_VARIABLE_FOR_IMPORTED_DATA = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet",
    "YVariableForImportedData",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="YVariableForImportedData")
    CastSelf = TypeVar(
        "CastSelf", bound="YVariableForImportedData._Cast_YVariableForImportedData"
    )


__docformat__ = "restructuredtext en"
__all__ = ("YVariableForImportedData",)


class YVariableForImportedData(Enum):
    """YVariableForImportedData

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _Y_VARIABLE_FOR_IMPORTED_DATA

    PRESSURE_RATIO = 0
    BOOST_PRESSURE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


YVariableForImportedData.__setattr__ = __enum_setattr
YVariableForImportedData.__delattr__ = __enum_delattr
