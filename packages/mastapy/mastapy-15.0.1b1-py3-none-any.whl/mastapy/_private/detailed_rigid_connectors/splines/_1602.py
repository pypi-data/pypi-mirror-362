"""SplineRatingTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SPLINE_RATING_TYPES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "SplineRatingTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SplineRatingTypes")
    CastSelf = TypeVar("CastSelf", bound="SplineRatingTypes._Cast_SplineRatingTypes")


__docformat__ = "restructuredtext en"
__all__ = ("SplineRatingTypes",)


class SplineRatingTypes(Enum):
    """SplineRatingTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SPLINE_RATING_TYPES

    GBT_178551999 = 0
    SAE_B9211996 = 1
    DIN_5466 = 2
    AGMA_6123C16 = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SplineRatingTypes.__setattr__ = __enum_setattr
SplineRatingTypes.__delattr__ = __enum_delattr
