"""GriddedSurface"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GRIDDED_SURFACE = python_net_import("SMT.MastaAPI.MathUtility", "GriddedSurface")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1694

    Self = TypeVar("Self", bound="GriddedSurface")
    CastSelf = TypeVar("CastSelf", bound="GriddedSurface._Cast_GriddedSurface")


__docformat__ = "restructuredtext en"
__all__ = ("GriddedSurface",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GriddedSurface:
    """Special nested class for casting GriddedSurface to subclasses."""

    __parent__: "GriddedSurface"

    @property
    def gridded_surface(self: "CastSelf") -> "GriddedSurface":
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
class GriddedSurface(_0.APIBase):
    """GriddedSurface

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GRIDDED_SURFACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def has_data(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasData")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def has_non_zero_data(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasNonZeroData")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_sorted(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsSorted")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def x_values(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XValues")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def y_values(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YValues")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def data_value_interpolated_at(
        self: "Self",
        row_value: "float",
        column_value: "float",
        row_extrapolation_option: "_1694.ExtrapolationOptions",
        column_extrapolation_option: "_1694.ExtrapolationOptions",
    ) -> "float":
        """float

        Args:
            row_value (float)
            column_value (float)
            row_extrapolation_option (mastapy.math_utility.ExtrapolationOptions)
            column_extrapolation_option (mastapy.math_utility.ExtrapolationOptions)
        """
        row_value = float(row_value)
        column_value = float(column_value)
        row_extrapolation_option = conversion.mp_to_pn_enum(
            row_extrapolation_option, "SMT.MastaAPI.MathUtility.ExtrapolationOptions"
        )
        column_extrapolation_option = conversion.mp_to_pn_enum(
            column_extrapolation_option, "SMT.MastaAPI.MathUtility.ExtrapolationOptions"
        )
        method_result = pythonnet_method_call(
            self.wrapped,
            "DataValueInterpolatedAt",
            row_value if row_value else 0.0,
            column_value if column_value else 0.0,
            row_extrapolation_option,
            column_extrapolation_option,
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def get_column(self: "Self", column_id: "int") -> "List[float]":
        """List[float]

        Args:
            column_id (int)
        """
        column_id = int(column_id)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "GetColumn", column_id if column_id else 0
            ),
            float,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_row(self: "Self", row_id: "int") -> "List[float]":
        """List[float]

        Args:
            row_id (int)
        """
        row_id = int(row_id)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "GetRow", row_id if row_id else 0),
            float,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_value(self: "Self", x_index: "int", y_index: "int") -> "float":
        """float

        Args:
            x_index (int)
            y_index (int)
        """
        x_index = int(x_index)
        y_index = int(y_index)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetValue",
            x_index if x_index else 0,
            y_index if y_index else 0,
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_GriddedSurface":
        """Cast to another type.

        Returns:
            _Cast_GriddedSurface
        """
        return _Cast_GriddedSurface(self)
