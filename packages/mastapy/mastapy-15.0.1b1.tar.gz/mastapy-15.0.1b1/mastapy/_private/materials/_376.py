"""TemperatureDependentProperty"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import (
    constructor,
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

_TEMPERATURE_DEPENDENT_PROPERTY = python_net_import(
    "SMT.MastaAPI.Materials", "TemperatureDependentProperty"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.math_utility import _1718
    from mastapy._private.utility.units_and_measurements import _1797
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="TemperatureDependentProperty")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TemperatureDependentProperty._Cast_TemperatureDependentProperty",
    )

T = TypeVar("T", bound="_1797.MeasurementBase")

__docformat__ = "restructuredtext en"
__all__ = ("TemperatureDependentProperty",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TemperatureDependentProperty:
    """Special nested class for casting TemperatureDependentProperty to subclasses."""

    __parent__: "TemperatureDependentProperty"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def temperature_dependent_property(
        self: "CastSelf",
    ) -> "TemperatureDependentProperty":
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
class TemperatureDependentProperty(
    _1779.IndependentReportablePropertiesBase["TemperatureDependentProperty"[T]]
):
    """TemperatureDependentProperty

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _TEMPERATURE_DEPENDENT_PROPERTY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def constant_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ConstantValue")

        if temp is None:
            return 0.0

        return temp

    @constant_value.setter
    @exception_bridge
    @enforce_parameter_types
    def constant_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ConstantValue", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def extrapolation(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions":
        """EnumWithSelectedValue[mastapy.math_utility.ExtrapolationOptions]"""
        temp = pythonnet_property_get(self.wrapped, "Extrapolation")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @extrapolation.setter
    @exception_bridge
    @enforce_parameter_types
    def extrapolation(self: "Self", value: "_1694.ExtrapolationOptions") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Extrapolation", value)

    @property
    @exception_bridge
    def is_constant(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsConstant")

        if temp is None:
            return False

        return temp

    @is_constant.setter
    @exception_bridge
    @enforce_parameter_types
    def is_constant(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsConstant", bool(value) if value is not None else False
        )

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
    @exception_bridge
    def vs_temperature(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "VsTemperature")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @vs_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def vs_temperature(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "VsTemperature", value.wrapped)

    @property
    @exception_bridge
    def vs_temperature_plot(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VsTemperaturePlot")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_TemperatureDependentProperty":
        """Cast to another type.

        Returns:
            _Cast_TemperatureDependentProperty
        """
        return _Cast_TemperatureDependentProperty(self)
