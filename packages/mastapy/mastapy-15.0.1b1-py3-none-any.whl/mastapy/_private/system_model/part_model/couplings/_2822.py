"""ConceptCouplingHalfPositioning"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_POSITIONING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCouplingHalfPositioning"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConceptCouplingHalfPositioning")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConceptCouplingHalfPositioning._Cast_ConceptCouplingHalfPositioning",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptCouplingHalfPositioning",)


class ConceptCouplingHalfPositioning(Enum):
    """ConceptCouplingHalfPositioning

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CONCEPT_COUPLING_HALF_POSITIONING

    HALVES_ARE_COINCIDENT = 0
    HALVES_ARE_CONCENTRIC = 1
    HALVES_FREELY_POSITIONED = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ConceptCouplingHalfPositioning.__setattr__ = __enum_setattr
ConceptCouplingHalfPositioning.__delattr__ = __enum_delattr
