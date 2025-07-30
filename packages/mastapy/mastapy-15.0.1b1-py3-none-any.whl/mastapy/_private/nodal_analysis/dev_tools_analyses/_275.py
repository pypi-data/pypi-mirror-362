"""FEModelSetupViewType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FE_MODEL_SETUP_VIEW_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "FEModelSetupViewType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEModelSetupViewType")
    CastSelf = TypeVar(
        "CastSelf", bound="FEModelSetupViewType._Cast_FEModelSetupViewType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEModelSetupViewType",)


class FEModelSetupViewType(Enum):
    """FEModelSetupViewType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FE_MODEL_SETUP_VIEW_TYPE

    CURRENT_SETUP = 0
    REDUCTION_RESULT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FEModelSetupViewType.__setattr__ = __enum_setattr
FEModelSetupViewType.__delattr__ = __enum_delattr
