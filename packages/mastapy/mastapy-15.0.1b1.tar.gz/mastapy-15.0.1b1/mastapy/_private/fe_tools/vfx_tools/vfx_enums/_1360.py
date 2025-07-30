"""ProSolveEigenmethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PRO_SOLVE_EIGENMETHOD = python_net_import(
    "SMT.MastaAPI.FETools.VfxTools.VfxEnums", "ProSolveEigenmethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ProSolveEigenmethod")
    CastSelf = TypeVar(
        "CastSelf", bound="ProSolveEigenmethod._Cast_ProSolveEigenmethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ProSolveEigenmethod",)


class ProSolveEigenmethod(Enum):
    """ProSolveEigenmethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PRO_SOLVE_EIGENMETHOD

    LANCZOS = 6
    AMLS = 9


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ProSolveEigenmethod.__setattr__ = __enum_setattr
ProSolveEigenmethod.__delattr__ = __enum_delattr
