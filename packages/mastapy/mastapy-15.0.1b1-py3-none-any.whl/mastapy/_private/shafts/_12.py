"""FkmSnCurveModel"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FKM_SN_CURVE_MODEL = python_net_import("SMT.MastaAPI.Shafts", "FkmSnCurveModel")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FkmSnCurveModel")
    CastSelf = TypeVar("CastSelf", bound="FkmSnCurveModel._Cast_FkmSnCurveModel")


__docformat__ = "restructuredtext en"
__all__ = ("FkmSnCurveModel",)


class FkmSnCurveModel(Enum):
    """FkmSnCurveModel

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FKM_SN_CURVE_MODEL

    MODEL_I = 0
    MODEL_II = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FkmSnCurveModel.__setattr__ = __enum_setattr
FkmSnCurveModel.__delattr__ = __enum_delattr
