"""FluxBarriers"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FLUX_BARRIERS = python_net_import("SMT.MastaAPI.ElectricMachines", "FluxBarriers")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FluxBarriers")
    CastSelf = TypeVar("CastSelf", bound="FluxBarriers._Cast_FluxBarriers")


__docformat__ = "restructuredtext en"
__all__ = ("FluxBarriers",)


class FluxBarriers(Enum):
    """FluxBarriers

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FLUX_BARRIERS

    NO_FLUX_BARRIERS = 0
    INNER_FLUX_BARRIERS_ONLY = 1
    OUTER_FLUX_BARRIERS_ONLY = 2
    INNER_AND_OUTER_FLUX_BARRIERS = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FluxBarriers.__setattr__ = __enum_setattr
FluxBarriers.__delattr__ = __enum_delattr
