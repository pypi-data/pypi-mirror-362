"""GriddedSurfaceAccessor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from clr import GetClrType

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ARRAY = python_net_import("System", "Array")
_DOUBLE = python_net_import("System", "Double")
_GRIDDED_SURFACE_ACCESSOR = python_net_import(
    "SMT.MastaAPI.MathUtility.MeasuredData", "GriddedSurfaceAccessor"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1699

    Self = TypeVar("Self", bound="GriddedSurfaceAccessor")
    CastSelf = TypeVar(
        "CastSelf", bound="GriddedSurfaceAccessor._Cast_GriddedSurfaceAccessor"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GriddedSurfaceAccessor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GriddedSurfaceAccessor:
    """Special nested class for casting GriddedSurfaceAccessor to subclasses."""

    __parent__: "GriddedSurfaceAccessor"

    @property
    def gridded_surface_accessor(self: "CastSelf") -> "GriddedSurfaceAccessor":
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
class GriddedSurfaceAccessor(_0.APIBase):
    """GriddedSurfaceAccessor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GRIDDED_SURFACE_ACCESSOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    @enforce_parameter_types
    def create_new_from_gridded_data(
        self: "Self", x_values: "List[float]", y_values: "List[float]"
    ) -> "GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor

        Args:
            x_values (List[float])
            y_values (List[float])
        """
        x_values = conversion.mp_to_pn_array_float(x_values)
        y_values = conversion.mp_to_pn_array_float(y_values)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "CreateNewFromGriddedData",
            [_ARRAY[_DOUBLE], _ARRAY[_DOUBLE]],
            x_values,
            y_values,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def create_new_from_gridded_data_3d(
        self: "Self",
        x_values: "List[float]",
        y_values: "List[float]",
        z_values: "List[List[float]]",
    ) -> "GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor

        Args:
            x_values (List[float])
            y_values (List[float])
            z_values (List[List[float]])
        """
        x_values = conversion.mp_to_pn_array_float(x_values)
        y_values = conversion.mp_to_pn_array_float(y_values)
        z_values = conversion.mp_to_pn_list_float_2d(z_values)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "CreateNewFromGriddedData",
            [_ARRAY[_DOUBLE], _ARRAY[_DOUBLE], GetClrType(_DOUBLE).MakeArrayType(2)],
            x_values,
            y_values,
            z_values,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def create_new_from_gridded_surface(
        self: "Self", grid: "_1699.GriddedSurface"
    ) -> "GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor

        Args:
            grid (mastapy.math_utility.GriddedSurface)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "CreateNewFromGriddedSurface", grid.wrapped if grid else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def get_gridded_surface(self: "Self") -> "_1699.GriddedSurface":
        """mastapy.math_utility.GriddedSurface"""
        method_result = pythonnet_method_call(self.wrapped, "GetGriddedSurface")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GriddedSurfaceAccessor":
        """Cast to another type.

        Returns:
            _Cast_GriddedSurfaceAccessor
        """
        return _Cast_GriddedSurfaceAccessor(self)
