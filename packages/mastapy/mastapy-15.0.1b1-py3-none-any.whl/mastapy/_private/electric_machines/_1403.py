"""FluxBarrierStyle"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FLUX_BARRIER_STYLE = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "FluxBarrierStyle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FluxBarrierStyle")
    CastSelf = TypeVar("CastSelf", bound="FluxBarrierStyle._Cast_FluxBarrierStyle")


__docformat__ = "restructuredtext en"
__all__ = ("FluxBarrierStyle",)


class FluxBarrierStyle(Enum):
    """FluxBarrierStyle

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FLUX_BARRIER_STYLE

    BRIDGE = 0
    CIRCULAR = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FluxBarrierStyle.__setattr__ = __enum_setattr
FluxBarrierStyle.__delattr__ = __enum_delattr
