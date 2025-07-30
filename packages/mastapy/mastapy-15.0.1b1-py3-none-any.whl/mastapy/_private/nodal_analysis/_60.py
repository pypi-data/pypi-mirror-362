"""DiagonalNonLinearStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DIAGONAL_NON_LINEAR_STIFFNESS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "DiagonalNonLinearStiffness"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1718

    Self = TypeVar("Self", bound="DiagonalNonLinearStiffness")
    CastSelf = TypeVar(
        "CastSelf", bound="DiagonalNonLinearStiffness._Cast_DiagonalNonLinearStiffness"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DiagonalNonLinearStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DiagonalNonLinearStiffness:
    """Special nested class for casting DiagonalNonLinearStiffness to subclasses."""

    __parent__: "DiagonalNonLinearStiffness"

    @property
    def diagonal_non_linear_stiffness(self: "CastSelf") -> "DiagonalNonLinearStiffness":
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
class DiagonalNonLinearStiffness(_0.APIBase):
    """DiagonalNonLinearStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DIAGONAL_NON_LINEAR_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def theta_x_stiffness(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "ThetaXStiffness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @theta_x_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def theta_x_stiffness(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "ThetaXStiffness", value.wrapped)

    @property
    @exception_bridge
    def theta_y_stiffness(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "ThetaYStiffness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @theta_y_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def theta_y_stiffness(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "ThetaYStiffness", value.wrapped)

    @property
    @exception_bridge
    def theta_z_stiffness(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "ThetaZStiffness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @theta_z_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def theta_z_stiffness(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "ThetaZStiffness", value.wrapped)

    @property
    @exception_bridge
    def x_stiffness(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "XStiffness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @x_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def x_stiffness(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "XStiffness", value.wrapped)

    @property
    @exception_bridge
    def y_stiffness(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "YStiffness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @y_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def y_stiffness(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "YStiffness", value.wrapped)

    @property
    @exception_bridge
    def z_stiffness(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "ZStiffness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @z_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def z_stiffness(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "ZStiffness", value.wrapped)

    @property
    def cast_to(self: "Self") -> "_Cast_DiagonalNonLinearStiffness":
        """Cast to another type.

        Returns:
            _Cast_DiagonalNonLinearStiffness
        """
        return _Cast_DiagonalNonLinearStiffness(self)
