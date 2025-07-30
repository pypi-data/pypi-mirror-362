"""FrictionModelForGyroscopicMoment"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FRICTION_MODEL_FOR_GYROSCOPIC_MOMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "FrictionModelForGyroscopicMoment"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FrictionModelForGyroscopicMoment")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FrictionModelForGyroscopicMoment._Cast_FrictionModelForGyroscopicMoment",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FrictionModelForGyroscopicMoment",)


class FrictionModelForGyroscopicMoment(Enum):
    """FrictionModelForGyroscopicMoment

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FRICTION_MODEL_FOR_GYROSCOPIC_MOMENT

    OUTER_RACEWAY_CONTROL = 0
    INNER_RACEWAY_CONTROL = 1
    HYBRID_MODEL = 2
    ADAPTIVE_RACEWAY_CONTROL = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FrictionModelForGyroscopicMoment.__setattr__ = __enum_setattr
FrictionModelForGyroscopicMoment.__delattr__ = __enum_delattr
