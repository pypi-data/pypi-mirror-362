"""ComponentDampingOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COMPONENT_DAMPING_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel", "ComponentDampingOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ComponentDampingOption")
    CastSelf = TypeVar(
        "CastSelf", bound="ComponentDampingOption._Cast_ComponentDampingOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentDampingOption",)


class ComponentDampingOption(Enum):
    """ComponentDampingOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COMPONENT_DAMPING_OPTION

    LOAD_CASE_GLOBAL_DAMPING = 0
    SPECIFIED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ComponentDampingOption.__setattr__ = __enum_setattr
ComponentDampingOption.__delattr__ = __enum_delattr
