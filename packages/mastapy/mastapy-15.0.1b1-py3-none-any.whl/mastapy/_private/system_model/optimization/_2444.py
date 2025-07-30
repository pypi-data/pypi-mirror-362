"""OptimizationParameter"""

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

_OPTIMIZATION_PARAMETER = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization", "OptimizationParameter"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OptimizationParameter")
    CastSelf = TypeVar(
        "CastSelf", bound="OptimizationParameter._Cast_OptimizationParameter"
    )


__docformat__ = "restructuredtext en"
__all__ = ("OptimizationParameter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OptimizationParameter:
    """Special nested class for casting OptimizationParameter to subclasses."""

    __parent__: "OptimizationParameter"

    @property
    def optimization_parameter(self: "CastSelf") -> "OptimizationParameter":
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
class OptimizationParameter(_0.APIBase):
    """OptimizationParameter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OPTIMIZATION_PARAMETER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def description(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Description")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_OptimizationParameter":
        """Cast to another type.

        Returns:
            _Cast_OptimizationParameter
        """
        return _Cast_OptimizationParameter(self)
