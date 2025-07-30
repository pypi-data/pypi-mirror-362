"""SplineDesignTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SPLINE_DESIGN_TYPES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "SplineDesignTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SplineDesignTypes")
    CastSelf = TypeVar("CastSelf", bound="SplineDesignTypes._Cast_SplineDesignTypes")


__docformat__ = "restructuredtext en"
__all__ = ("SplineDesignTypes",)


class SplineDesignTypes(Enum):
    """SplineDesignTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SPLINE_DESIGN_TYPES

    DIN_548012006 = 0
    ISO_4156122005 = 1
    GBT_347812008 = 2
    JIS_B_16032001 = 3
    SAE_B9211996 = 4
    CUSTOM = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SplineDesignTypes.__setattr__ = __enum_setattr
SplineDesignTypes.__delattr__ = __enum_delattr
