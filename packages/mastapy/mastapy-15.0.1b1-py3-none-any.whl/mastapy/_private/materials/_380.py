"""WindTurbineStandards"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_WIND_TURBINE_STANDARDS = python_net_import(
    "SMT.MastaAPI.Materials", "WindTurbineStandards"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WindTurbineStandards")
    CastSelf = TypeVar(
        "CastSelf", bound="WindTurbineStandards._Cast_WindTurbineStandards"
    )


__docformat__ = "restructuredtext en"
__all__ = ("WindTurbineStandards",)


class WindTurbineStandards(Enum):
    """WindTurbineStandards

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _WIND_TURBINE_STANDARDS

    NONE = 0
    GL = 1
    ISO_814004 = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


WindTurbineStandards.__setattr__ = __enum_setattr
WindTurbineStandards.__delattr__ = __enum_delattr
