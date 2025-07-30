"""TiltingPadThrustBearing"""

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
from mastapy._private.bearings.bearing_designs.fluid_film import _2398

_TILTING_PAD_THRUST_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm", "TiltingPadThrustBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings import _2080, _2103
    from mastapy._private.bearings.bearing_designs import _2340, _2341, _2344

    Self = TypeVar("Self", bound="TiltingPadThrustBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="TiltingPadThrustBearing._Cast_TiltingPadThrustBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TiltingPadThrustBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TiltingPadThrustBearing:
    """Special nested class for casting TiltingPadThrustBearing to subclasses."""

    __parent__: "TiltingPadThrustBearing"

    @property
    def pad_fluid_film_bearing(self: "CastSelf") -> "_2398.PadFluidFilmBearing":
        return self.__parent__._cast(_2398.PadFluidFilmBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2341.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2341

        return self.__parent__._cast(_2341.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2344.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2344

        return self.__parent__._cast(_2344.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2340.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2340

        return self.__parent__._cast(_2340.BearingDesign)

    @property
    def tilting_pad_thrust_bearing(self: "CastSelf") -> "TiltingPadThrustBearing":
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
class TiltingPadThrustBearing(_2398.PadFluidFilmBearing):
    """TiltingPadThrustBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TILTING_PAD_THRUST_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def model(self: "Self") -> "_2080.BearingModel":
        """mastapy.bearings.BearingModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Model")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.BearingModel")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2080", "BearingModel"
        )(value)

    @property
    @exception_bridge
    def non_dimensional_friction(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalFriction")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @non_dimensional_friction.setter
    @exception_bridge
    @enforce_parameter_types
    def non_dimensional_friction(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NonDimensionalFriction", value)

    @property
    @exception_bridge
    def non_dimensional_inlet_flow(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalInletFlow")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @non_dimensional_inlet_flow.setter
    @exception_bridge
    @enforce_parameter_types
    def non_dimensional_inlet_flow(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NonDimensionalInletFlow", value)

    @property
    @exception_bridge
    def non_dimensional_load(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalLoad")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @non_dimensional_load.setter
    @exception_bridge
    @enforce_parameter_types
    def non_dimensional_load(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NonDimensionalLoad", value)

    @property
    @exception_bridge
    def non_dimensional_minimum_film_thickness(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "NonDimensionalMinimumFilmThickness"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @non_dimensional_minimum_film_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def non_dimensional_minimum_film_thickness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "NonDimensionalMinimumFilmThickness", value
        )

    @property
    @exception_bridge
    def non_dimensional_side_flow(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalSideFlow")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @non_dimensional_side_flow.setter
    @exception_bridge
    @enforce_parameter_types
    def non_dimensional_side_flow(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NonDimensionalSideFlow", value)

    @property
    @exception_bridge
    def pad_circumferential_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PadCircumferentialWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pad_height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PadHeight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pad_height_aspect_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PadHeightAspectRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pad_inner_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PadInnerDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pad_inner_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def pad_inner_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PadInnerDiameter", value)

    @property
    @exception_bridge
    def pad_outer_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PadOuterDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pad_outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def pad_outer_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PadOuterDiameter", value)

    @property
    @exception_bridge
    def pad_width_aspect_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PadWidthAspectRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pivot_angular_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PivotAngularOffset")

        if temp is None:
            return 0.0

        return temp

    @pivot_angular_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def pivot_angular_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PivotAngularOffset",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tilting_pad_type(self: "Self") -> "_2103.TiltingPadTypes":
        """mastapy.bearings.TiltingPadTypes"""
        temp = pythonnet_property_get(self.wrapped, "TiltingPadType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.TiltingPadTypes")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2103", "TiltingPadTypes"
        )(value)

    @tilting_pad_type.setter
    @exception_bridge
    @enforce_parameter_types
    def tilting_pad_type(self: "Self", value: "_2103.TiltingPadTypes") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Bearings.TiltingPadTypes")
        pythonnet_property_set(self.wrapped, "TiltingPadType", value)

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TiltingPadThrustBearing":
        """Cast to another type.

        Returns:
            _Cast_TiltingPadThrustBearing
        """
        return _Cast_TiltingPadThrustBearing(self)
