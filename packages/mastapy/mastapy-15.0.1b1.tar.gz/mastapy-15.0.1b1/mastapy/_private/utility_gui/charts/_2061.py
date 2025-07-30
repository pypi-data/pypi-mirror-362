"""ModeConstantLine"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility_gui.charts import _2056

_MODE_CONSTANT_LINE = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Charts", "ModeConstantLine"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ModeConstantLine")
    CastSelf = TypeVar("CastSelf", bound="ModeConstantLine._Cast_ModeConstantLine")


__docformat__ = "restructuredtext en"
__all__ = ("ModeConstantLine",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModeConstantLine:
    """Special nested class for casting ModeConstantLine to subclasses."""

    __parent__: "ModeConstantLine"

    @property
    def constant_line(self: "CastSelf") -> "_2056.ConstantLine":
        return self.__parent__._cast(_2056.ConstantLine)

    @property
    def mode_constant_line(self: "CastSelf") -> "ModeConstantLine":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class ModeConstantLine(_2056.ConstantLine):
    """ModeConstantLine

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODE_CONSTANT_LINE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ModeConstantLine":
        """Cast to another type.

        Returns:
            _Cast_ModeConstantLine
        """
        return _Cast_ModeConstantLine(self)
