"""ImportType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_IMPORT_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ImportType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ImportType")
    CastSelf = TypeVar("CastSelf", bound="ImportType._Cast_ImportType")


__docformat__ = "restructuredtext en"
__all__ = ("ImportType",)


class ImportType(Enum):
    """ImportType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _IMPORT_TYPE

    DUTY_CYCLE_TIME_SERIES = 0
    INDIVIDUAL_LOAD_CASE = 1
    INDIVIDUAL_LOAD_CASES_AS_TIME_SERIES = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ImportType.__setattr__ = __enum_setattr
ImportType.__delattr__ = __enum_delattr
