"""PadFluidFilmBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings import _2100
from mastapy._private.bearings.bearing_designs import _2341

_PAD_FLUID_FILM_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm", "PadFluidFilmBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2340, _2344
    from mastapy._private.bearings.bearing_designs.fluid_film import _2405, _2406

    Self = TypeVar("Self", bound="PadFluidFilmBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="PadFluidFilmBearing._Cast_PadFluidFilmBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PadFluidFilmBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PadFluidFilmBearing:
    """Special nested class for casting PadFluidFilmBearing to subclasses."""

    __parent__: "PadFluidFilmBearing"

    @property
    def detailed_bearing(self: "CastSelf") -> "_2341.DetailedBearing":
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
    def tilting_pad_journal_bearing(
        self: "CastSelf",
    ) -> "_2405.TiltingPadJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2405

        return self.__parent__._cast(_2405.TiltingPadJournalBearing)

    @property
    def tilting_pad_thrust_bearing(self: "CastSelf") -> "_2406.TiltingPadThrustBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2406

        return self.__parent__._cast(_2406.TiltingPadThrustBearing)

    @property
    def pad_fluid_film_bearing(self: "CastSelf") -> "PadFluidFilmBearing":
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
class PadFluidFilmBearing(_2341.DetailedBearing):
    """PadFluidFilmBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PAD_FLUID_FILM_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def collar_surface_roughness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CollarSurfaceRoughness")

        if temp is None:
            return 0.0

        return temp

    @collar_surface_roughness.setter
    @exception_bridge
    @enforce_parameter_types
    def collar_surface_roughness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CollarSurfaceRoughness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def limiting_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LimitingFilmThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_pads(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPads")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_pads.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_pads(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfPads", value)

    @property
    @exception_bridge
    def pad_angular_extent(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PadAngularExtent")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pad_angular_extent.setter
    @exception_bridge
    @enforce_parameter_types
    def pad_angular_extent(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PadAngularExtent", value)

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
    def rotational_direction(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RotationalDirections":
        """EnumWithSelectedValue[mastapy.bearings.RotationalDirections]"""
        temp = pythonnet_property_get(self.wrapped, "RotationalDirection")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RotationalDirections.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @rotational_direction.setter
    @exception_bridge
    @enforce_parameter_types
    def rotational_direction(self: "Self", value: "_2100.RotationalDirections") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RotationalDirections.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "RotationalDirection", value)

    @property
    def cast_to(self: "Self") -> "_Cast_PadFluidFilmBearing":
        """Cast to another type.

        Returns:
            _Cast_PadFluidFilmBearing
        """
        return _Cast_PadFluidFilmBearing(self)
