"""ConceptCouplingSpeedRatioSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CONCEPT_COUPLING_SPEED_RATIO_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.SystemModel", "ConceptCouplingSpeedRatioSpecificationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConceptCouplingSpeedRatioSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConceptCouplingSpeedRatioSpecificationMethod._Cast_ConceptCouplingSpeedRatioSpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptCouplingSpeedRatioSpecificationMethod",)


class ConceptCouplingSpeedRatioSpecificationMethod(Enum):
    """ConceptCouplingSpeedRatioSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CONCEPT_COUPLING_SPEED_RATIO_SPECIFICATION_METHOD

    FIXED = 0
    VARYING_WITH_TIME = 1
    PID_CONTROL = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ConceptCouplingSpeedRatioSpecificationMethod.__setattr__ = __enum_setattr
ConceptCouplingSpeedRatioSpecificationMethod.__delattr__ = __enum_delattr
