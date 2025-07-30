"""MicroGeometryOptimisationTarget"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MICRO_GEOMETRY_OPTIMISATION_TARGET = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization", "MicroGeometryOptimisationTarget"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MicroGeometryOptimisationTarget")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicroGeometryOptimisationTarget._Cast_MicroGeometryOptimisationTarget",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryOptimisationTarget",)


class MicroGeometryOptimisationTarget(Enum):
    """MicroGeometryOptimisationTarget

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MICRO_GEOMETRY_OPTIMISATION_TARGET

    TRANSMISSION_ERROR = 0
    CONTACT_STRESS = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MicroGeometryOptimisationTarget.__setattr__ = __enum_setattr
MicroGeometryOptimisationTarget.__delattr__ = __enum_delattr
