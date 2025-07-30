"""SplineFixtureTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SPLINE_FIXTURE_TYPES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "SplineFixtureTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SplineFixtureTypes")
    CastSelf = TypeVar("CastSelf", bound="SplineFixtureTypes._Cast_SplineFixtureTypes")


__docformat__ = "restructuredtext en"
__all__ = ("SplineFixtureTypes",)


class SplineFixtureTypes(Enum):
    """SplineFixtureTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SPLINE_FIXTURE_TYPES

    FLEXIBLE = 0
    FIXED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SplineFixtureTypes.__setattr__ = __enum_setattr
SplineFixtureTypes.__delattr__ = __enum_delattr
