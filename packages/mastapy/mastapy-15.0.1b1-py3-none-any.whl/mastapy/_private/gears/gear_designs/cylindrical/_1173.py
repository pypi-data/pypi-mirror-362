"""Micropitting"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.gears import _428
from mastapy._private.utility import _1779

_MICROPITTING = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "Micropitting"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Micropitting")
    CastSelf = TypeVar("CastSelf", bound="Micropitting._Cast_Micropitting")


__docformat__ = "restructuredtext en"
__all__ = ("Micropitting",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Micropitting:
    """Special nested class for casting Micropitting to subclasses."""

    __parent__: "Micropitting"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def micropitting(self: "CastSelf") -> "Micropitting":
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
class Micropitting(_1779.IndependentReportablePropertiesBase["Micropitting"]):
    """Micropitting

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICROPITTING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def estimate_bulk_temperature(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "EstimateBulkTemperature")

        if temp is None:
            return False

        return temp

    @estimate_bulk_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def estimate_bulk_temperature(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EstimateBulkTemperature",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def method_a_coefficient_of_friction_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod":
        """EnumWithSelectedValue[mastapy.gears.MicropittingCoefficientOfFrictionCalculationMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "MethodACoefficientOfFrictionMethod"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @method_a_coefficient_of_friction_method.setter
    @exception_bridge
    @enforce_parameter_types
    def method_a_coefficient_of_friction_method(
        self: "Self", value: "_428.MicropittingCoefficientOfFrictionCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "MethodACoefficientOfFrictionMethod", value
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Micropitting":
        """Cast to another type.

        Returns:
            _Cast_Micropitting
        """
        return _Cast_Micropitting(self)
