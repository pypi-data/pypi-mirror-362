"""Vector2DListAccessor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_2d import Vector2D

_VECTOR_2D_LIST_ACCESSOR = python_net_import(
    "SMT.MastaAPI.MathUtility", "Vector2DListAccessor"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="Vector2DListAccessor")
    CastSelf = TypeVar(
        "CastSelf", bound="Vector2DListAccessor._Cast_Vector2DListAccessor"
    )


__docformat__ = "restructuredtext en"
__all__ = ("Vector2DListAccessor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Vector2DListAccessor:
    """Special nested class for casting Vector2DListAccessor to subclasses."""

    __parent__: "Vector2DListAccessor"

    @property
    def vector_2d_list_accessor(self: "CastSelf") -> "Vector2DListAccessor":
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
class Vector2DListAccessor(_0.APIBase):
    """Vector2DListAccessor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VECTOR_2D_LIST_ACCESSOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    @enforce_parameter_types
    def create_new_from_vector_list(
        self: "Self", list: "List[Vector2D]"
    ) -> "Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor

        Args:
            list (List[Vector2D])
        """
        list = conversion.mp_to_pn_objects_in_dotnet_list(list)
        method_result = pythonnet_method_call(
            self.wrapped, "CreateNewFromVectorList", list
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def get_vector_list(self: "Self") -> "List[Vector2D]":
        """List[Vector2D]"""
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "GetVectorList"), Vector2D
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Vector2DListAccessor":
        """Cast to another type.

        Returns:
            _Cast_Vector2DListAccessor
        """
        return _Cast_Vector2DListAccessor(self)
