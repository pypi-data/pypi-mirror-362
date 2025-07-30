"""IWrapSMTType"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_I_WRAP_SMT_TYPE = python_net_import("SMT.MastaAPIUtility.Scripting", "IWrapSMTType")

if TYPE_CHECKING:
    from typing import TypeVar

    Self = TypeVar("Self", bound="IWrapSMTType")


__docformat__ = "restructuredtext en"
__all__ = ("IWrapSMTType",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class IWrapSMTType:
    """This class is a public interface.
    The class body has intentionally been left empty.
    """
