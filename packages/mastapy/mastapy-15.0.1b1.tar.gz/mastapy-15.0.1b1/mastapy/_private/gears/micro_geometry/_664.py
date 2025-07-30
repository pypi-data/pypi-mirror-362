"""LocationOfEvaluationLowerLimit"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LOCATION_OF_EVALUATION_LOWER_LIMIT = python_net_import(
    "SMT.MastaAPI.Gears.MicroGeometry", "LocationOfEvaluationLowerLimit"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LocationOfEvaluationLowerLimit")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LocationOfEvaluationLowerLimit._Cast_LocationOfEvaluationLowerLimit",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LocationOfEvaluationLowerLimit",)


class LocationOfEvaluationLowerLimit(Enum):
    """LocationOfEvaluationLowerLimit

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LOCATION_OF_EVALUATION_LOWER_LIMIT

    USERSPECIFIED = 0
    ROOT_FORM = 1
    START_OF_ROOT_RELIEF = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LocationOfEvaluationLowerLimit.__setattr__ = __enum_setattr
LocationOfEvaluationLowerLimit.__delattr__ = __enum_delattr
