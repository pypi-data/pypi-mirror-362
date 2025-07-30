"""AllRingPinsManufacturingError"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ALL_RING_PINS_MANUFACTURING_ERROR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AllRingPinsManufacturingError",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.tolerances import _2121
    from mastapy._private.system_model.analyses_and_results.static_loads import _7813

    Self = TypeVar("Self", bound="AllRingPinsManufacturingError")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AllRingPinsManufacturingError._Cast_AllRingPinsManufacturingError",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AllRingPinsManufacturingError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AllRingPinsManufacturingError:
    """Special nested class for casting AllRingPinsManufacturingError to subclasses."""

    __parent__: "AllRingPinsManufacturingError"

    @property
    def all_ring_pins_manufacturing_error(
        self: "CastSelf",
    ) -> "AllRingPinsManufacturingError":
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
class AllRingPinsManufacturingError(_0.APIBase):
    """AllRingPinsManufacturingError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ALL_RING_PINS_MANUFACTURING_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def all_pins_roundness_chart(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllPinsRoundnessChart")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def angular_position_error_for_all_pins(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngularPositionErrorForAllPins")

        if temp is None:
            return 0.0

        return temp

    @angular_position_error_for_all_pins.setter
    @exception_bridge
    @enforce_parameter_types
    def angular_position_error_for_all_pins(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AngularPositionErrorForAllPins",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pin_diameter_error_for_all_pins(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinDiameterErrorForAllPins")

        if temp is None:
            return 0.0

        return temp

    @pin_diameter_error_for_all_pins.setter
    @exception_bridge
    @enforce_parameter_types
    def pin_diameter_error_for_all_pins(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinDiameterErrorForAllPins",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def radial_position_error_for_all_pins(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialPositionErrorForAllPins")

        if temp is None:
            return 0.0

        return temp

    @radial_position_error_for_all_pins.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_position_error_for_all_pins(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialPositionErrorForAllPins",
            float(value) if value is not None else 0.0,
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
    @exception_bridge
    def ring_pin_manufacturing_errors(
        self: "Self",
    ) -> "List[_7813.RingPinManufacturingError]":
        """List[mastapy.system_model.analyses_and_results.static_loads.RingPinManufacturingError]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingPinManufacturingErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AllRingPinsManufacturingError":
        """Cast to another type.

        Returns:
            _Cast_AllRingPinsManufacturingError
        """
        return _Cast_AllRingPinsManufacturingError(self)
