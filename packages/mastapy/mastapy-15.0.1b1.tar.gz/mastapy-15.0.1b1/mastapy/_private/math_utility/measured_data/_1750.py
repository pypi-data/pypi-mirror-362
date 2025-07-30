"""LookupTableBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import (
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility import _1694
from mastapy._private.utility import _1779

_LOOKUP_TABLE_BASE = python_net_import(
    "SMT.MastaAPI.MathUtility.MeasuredData", "LookupTableBase"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.math_utility.measured_data import _1751, _1752

    Self = TypeVar("Self", bound="LookupTableBase")
    CastSelf = TypeVar("CastSelf", bound="LookupTableBase._Cast_LookupTableBase")

T = TypeVar("T", bound="LookupTableBase")

__docformat__ = "restructuredtext en"
__all__ = ("LookupTableBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LookupTableBase:
    """Special nested class for casting LookupTableBase to subclasses."""

    __parent__: "LookupTableBase"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def onedimensional_function_lookup_table(
        self: "CastSelf",
    ) -> "_1751.OnedimensionalFunctionLookupTable":
        from mastapy._private.math_utility.measured_data import _1751

        return self.__parent__._cast(_1751.OnedimensionalFunctionLookupTable)

    @property
    def twodimensional_function_lookup_table(
        self: "CastSelf",
    ) -> "_1752.TwodimensionalFunctionLookupTable":
        from mastapy._private.math_utility.measured_data import _1752

        return self.__parent__._cast(_1752.TwodimensionalFunctionLookupTable)

    @property
    def lookup_table_base(self: "CastSelf") -> "LookupTableBase":
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
class LookupTableBase(_1779.IndependentReportablePropertiesBase[T]):
    """LookupTableBase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _LOOKUP_TABLE_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def extrapolation_option(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions":
        """EnumWithSelectedValue[mastapy.math_utility.ExtrapolationOptions]"""
        temp = pythonnet_property_get(self.wrapped, "ExtrapolationOption")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @extrapolation_option.setter
    @exception_bridge
    @enforce_parameter_types
    def extrapolation_option(self: "Self", value: "_1694.ExtrapolationOptions") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ExtrapolationOption", value)

    @property
    def cast_to(self: "Self") -> "_Cast_LookupTableBase":
        """Cast to another type.

        Returns:
            _Cast_LookupTableBase
        """
        return _Cast_LookupTableBase(self)
