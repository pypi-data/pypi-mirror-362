"""FluxBarrierOrWeb"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FLUX_BARRIER_OR_WEB = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "FluxBarrierOrWeb"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FluxBarrierOrWeb")
    CastSelf = TypeVar("CastSelf", bound="FluxBarrierOrWeb._Cast_FluxBarrierOrWeb")


__docformat__ = "restructuredtext en"
__all__ = ("FluxBarrierOrWeb",)


class FluxBarrierOrWeb(Enum):
    """FluxBarrierOrWeb

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FLUX_BARRIER_OR_WEB

    FLUX_BARRIER = 0
    WEB = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FluxBarrierOrWeb.__setattr__ = __enum_setattr
FluxBarrierOrWeb.__delattr__ = __enum_delattr
