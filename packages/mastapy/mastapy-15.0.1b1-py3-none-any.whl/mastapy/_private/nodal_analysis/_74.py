"""IntegrationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_INTEGRATION_METHOD = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "IntegrationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="IntegrationMethod")
    CastSelf = TypeVar("CastSelf", bound="IntegrationMethod._Cast_IntegrationMethod")


__docformat__ = "restructuredtext en"
__all__ = ("IntegrationMethod",)


class IntegrationMethod(Enum):
    """IntegrationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _INTEGRATION_METHOD

    NEWMARK = 0
    WILSON_THETA = 1
    BACKWARD_EULER_VELOCITY = 2
    LOBATTO3C_ORDER_2 = 3
    ESDIRK_ORDER_2 = 4
    ESDIRK_ORDER_4 = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


IntegrationMethod.__setattr__ = __enum_setattr
IntegrationMethod.__delattr__ = __enum_delattr
