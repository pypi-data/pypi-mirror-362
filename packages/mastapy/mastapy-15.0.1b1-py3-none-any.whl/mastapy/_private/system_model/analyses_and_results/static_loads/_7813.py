"""RingPinManufacturingError"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_RING_PIN_MANUFACTURING_ERROR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "RingPinManufacturingError",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.tolerances import _2121

    Self = TypeVar("Self", bound="RingPinManufacturingError")
    CastSelf = TypeVar(
        "CastSelf", bound="RingPinManufacturingError._Cast_RingPinManufacturingError"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RingPinManufacturingError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingPinManufacturingError:
    """Special nested class for casting RingPinManufacturingError to subclasses."""

    __parent__: "RingPinManufacturingError"

    @property
    def ring_pin_manufacturing_error(self: "CastSelf") -> "RingPinManufacturingError":
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
class RingPinManufacturingError(_0.APIBase):
    """RingPinManufacturingError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_PIN_MANUFACTURING_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def override_all_pins_roundness_specification(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "OverrideAllPinsRoundnessSpecification"
        )

        if temp is None:
            return False

        return temp

    @override_all_pins_roundness_specification.setter
    @exception_bridge
    @enforce_parameter_types
    def override_all_pins_roundness_specification(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideAllPinsRoundnessSpecification",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def pin_angular_position_error(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PinAngularPositionError")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pin_angular_position_error.setter
    @exception_bridge
    @enforce_parameter_types
    def pin_angular_position_error(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PinAngularPositionError", value)

    @property
    @exception_bridge
    def pin_diameter_error(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PinDiameterError")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pin_diameter_error.setter
    @exception_bridge
    @enforce_parameter_types
    def pin_diameter_error(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PinDiameterError", value)

    @property
    @exception_bridge
    def pin_radial_position_error(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PinRadialPositionError")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pin_radial_position_error.setter
    @exception_bridge
    @enforce_parameter_types
    def pin_radial_position_error(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PinRadialPositionError", value)

    @property
    @exception_bridge
    def pin_roundness_chart(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinRoundnessChart")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def show_pin_roundness_chart(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowPinRoundnessChart")

        if temp is None:
            return False

        return temp

    @show_pin_roundness_chart.setter
    @exception_bridge
    @enforce_parameter_types
    def show_pin_roundness_chart(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowPinRoundnessChart",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def roundness_specification(self: "Self") -> "_2121.RoundnessSpecification":
        """mastapy.bearings.tolerances.RoundnessSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoundnessSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RingPinManufacturingError":
        """Cast to another type.

        Returns:
            _Cast_RingPinManufacturingError
        """
        return _Cast_RingPinManufacturingError(self)
