"""NamedPoint"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_NAMED_POINT = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters.Tangibles", "NamedPoint"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NamedPoint")
    CastSelf = TypeVar("CastSelf", bound="NamedPoint._Cast_NamedPoint")


__docformat__ = "restructuredtext en"
__all__ = ("NamedPoint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NamedPoint:
    """Special nested class for casting NamedPoint to subclasses."""

    __parent__: "NamedPoint"

    @property
    def named_point(self: "CastSelf") -> "NamedPoint":
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
class NamedPoint(_0.APIBase):
    """NamedPoint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NAMED_POINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def x(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "X")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def y(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Y")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_NamedPoint":
        """Cast to another type.

        Returns:
            _Cast_NamedPoint
        """
        return _Cast_NamedPoint(self)
