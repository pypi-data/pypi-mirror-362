"""CoordinateSystemForWhine"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COORDINATE_SYSTEM_FOR_WHINE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "CoordinateSystemForWhine",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CoordinateSystemForWhine")
    CastSelf = TypeVar(
        "CastSelf", bound="CoordinateSystemForWhine._Cast_CoordinateSystemForWhine"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoordinateSystemForWhine",)


class CoordinateSystemForWhine(Enum):
    """CoordinateSystemForWhine

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COORDINATE_SYSTEM_FOR_WHINE

    LOCAL_COORDINATE_SYSTEM = 0
    GLOBAL_COORDINATE_SYSTEM = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CoordinateSystemForWhine.__setattr__ = __enum_setattr
CoordinateSystemForWhine.__delattr__ = __enum_delattr
