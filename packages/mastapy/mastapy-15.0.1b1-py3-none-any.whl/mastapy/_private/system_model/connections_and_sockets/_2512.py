"""RealignmentResult"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_REALIGNMENT_RESULT = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "RealignmentResult"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RealignmentResult")
    CastSelf = TypeVar("CastSelf", bound="RealignmentResult._Cast_RealignmentResult")


__docformat__ = "restructuredtext en"
__all__ = ("RealignmentResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RealignmentResult:
    """Special nested class for casting RealignmentResult to subclasses."""

    __parent__: "RealignmentResult"

    @property
    def realignment_result(self: "CastSelf") -> "RealignmentResult":
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
class RealignmentResult(_0.APIBase):
    """RealignmentResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REALIGNMENT_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def successful(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Successful")

        if temp is None:
            return False

        return temp

    @successful.setter
    @exception_bridge
    @enforce_parameter_types
    def successful(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Successful", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RealignmentResult":
        """Cast to another type.

        Returns:
            _Cast_RealignmentResult
        """
        return _Cast_RealignmentResult(self)
