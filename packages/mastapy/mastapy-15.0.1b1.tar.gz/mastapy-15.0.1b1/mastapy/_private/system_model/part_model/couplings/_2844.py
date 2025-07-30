"""SplinePitchErrorInputType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SPLINE_PITCH_ERROR_INPUT_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SplinePitchErrorInputType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SplinePitchErrorInputType")
    CastSelf = TypeVar(
        "CastSelf", bound="SplinePitchErrorInputType._Cast_SplinePitchErrorInputType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SplinePitchErrorInputType",)


class SplinePitchErrorInputType(Enum):
    """SplinePitchErrorInputType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SPLINE_PITCH_ERROR_INPUT_TYPE

    SINUSOIDAL = 0
    CUSTOM = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SplinePitchErrorInputType.__setattr__ = __enum_setattr
SplinePitchErrorInputType.__delattr__ = __enum_delattr
