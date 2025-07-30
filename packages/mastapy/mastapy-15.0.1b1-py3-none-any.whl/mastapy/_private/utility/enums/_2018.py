"""TableAndChartOptions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TABLE_AND_CHART_OPTIONS = python_net_import(
    "SMT.MastaAPI.Utility.Enums", "TableAndChartOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TableAndChartOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="TableAndChartOptions._Cast_TableAndChartOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TableAndChartOptions",)


class TableAndChartOptions(Enum):
    """TableAndChartOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TABLE_AND_CHART_OPTIONS

    CHART_THEN_TABLE = 0
    TABLE_THEN_CHART = 1
    TABLE = 2
    CHART = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TableAndChartOptions.__setattr__ = __enum_setattr
TableAndChartOptions.__delattr__ = __enum_delattr
