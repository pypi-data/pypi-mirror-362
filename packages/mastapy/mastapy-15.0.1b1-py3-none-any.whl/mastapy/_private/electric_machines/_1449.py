"""VShapedMagnetLayerSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.electric_machines import _1430

_V_SHAPED_MAGNET_LAYER_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "VShapedMagnetLayerSpecification"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.electric_machines import _1402, _1412

    Self = TypeVar("Self", bound="VShapedMagnetLayerSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VShapedMagnetLayerSpecification._Cast_VShapedMagnetLayerSpecification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VShapedMagnetLayerSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VShapedMagnetLayerSpecification:
    """Special nested class for casting VShapedMagnetLayerSpecification to subclasses."""

    __parent__: "VShapedMagnetLayerSpecification"

    @property
    def rotor_internal_layer_specification(
        self: "CastSelf",
    ) -> "_1430.RotorInternalLayerSpecification":
        return self.__parent__._cast(_1430.RotorInternalLayerSpecification)

    @property
    def v_shaped_magnet_layer_specification(
        self: "CastSelf",
    ) -> "VShapedMagnetLayerSpecification":
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
class VShapedMagnetLayerSpecification(_1430.RotorInternalLayerSpecification):
    """VShapedMagnetLayerSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _V_SHAPED_MAGNET_LAYER_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cutout_width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CutoutWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cutout_width.setter
    @exception_bridge
    @enforce_parameter_types
    def cutout_width(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CutoutWidth", value)

    @property
    @exception_bridge
    def distance_between_magnets(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DistanceBetweenMagnets")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @distance_between_magnets.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_between_magnets(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DistanceBetweenMagnets", value)

    @property
    @exception_bridge
    def distance_to_v_shape(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DistanceToVShape")

        if temp is None:
            return 0.0

        return temp

    @distance_to_v_shape.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_to_v_shape(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DistanceToVShape", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def flux_barrier_length(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FluxBarrierLength")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @flux_barrier_length.setter
    @exception_bridge
    @enforce_parameter_types
    def flux_barrier_length(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FluxBarrierLength", value)

    @property
    @exception_bridge
    def has_flux_barriers(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasFluxBarriers")

        if temp is None:
            return False

        return temp

    @has_flux_barriers.setter
    @exception_bridge
    @enforce_parameter_types
    def has_flux_barriers(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HasFluxBarriers", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def lower_round_height(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LowerRoundHeight")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @lower_round_height.setter
    @exception_bridge
    @enforce_parameter_types
    def lower_round_height(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LowerRoundHeight", value)

    @property
    @exception_bridge
    def magnet_clearance(self: "Self") -> "_1412.MagnetClearance":
        """mastapy.electric_machines.MagnetClearance"""
        temp = pythonnet_property_get(self.wrapped, "MagnetClearance")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.MagnetClearance"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1412", "MagnetClearance"
        )(value)

    @magnet_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def magnet_clearance(self: "Self", value: "_1412.MagnetClearance") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.MagnetClearance"
        )
        pythonnet_property_set(self.wrapped, "MagnetClearance", value)

    @property
    @exception_bridge
    def thickness_of_flux_barriers(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ThicknessOfFluxBarriers")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @thickness_of_flux_barriers.setter
    @exception_bridge
    @enforce_parameter_types
    def thickness_of_flux_barriers(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ThicknessOfFluxBarriers", value)

    @property
    @exception_bridge
    def upper_flux_barrier_web_specification(self: "Self") -> "_1402.FluxBarrierOrWeb":
        """mastapy.electric_machines.FluxBarrierOrWeb"""
        temp = pythonnet_property_get(self.wrapped, "UpperFluxBarrierWebSpecification")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.FluxBarrierOrWeb"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1402", "FluxBarrierOrWeb"
        )(value)

    @upper_flux_barrier_web_specification.setter
    @exception_bridge
    @enforce_parameter_types
    def upper_flux_barrier_web_specification(
        self: "Self", value: "_1402.FluxBarrierOrWeb"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.FluxBarrierOrWeb"
        )
        pythonnet_property_set(self.wrapped, "UpperFluxBarrierWebSpecification", value)

    @property
    @exception_bridge
    def upper_round_height(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "UpperRoundHeight")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @upper_round_height.setter
    @exception_bridge
    @enforce_parameter_types
    def upper_round_height(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UpperRoundHeight", value)

    @property
    @exception_bridge
    def v_shaped_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VShapedAngle")

        if temp is None:
            return 0.0

        return temp

    @v_shaped_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def v_shaped_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "VShapedAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def web_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WebLength")

        if temp is None:
            return 0.0

        return temp

    @web_length.setter
    @exception_bridge
    @enforce_parameter_types
    def web_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WebLength", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def web_thickness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "WebThickness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @web_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def web_thickness(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "WebThickness", value)

    @property
    def cast_to(self: "Self") -> "_Cast_VShapedMagnetLayerSpecification":
        """Cast to another type.

        Returns:
            _Cast_VShapedMagnetLayerSpecification
        """
        return _Cast_VShapedMagnetLayerSpecification(self)
