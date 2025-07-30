"""LoadedTiltingThrustPad"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_results.fluid_film import _2328

_LOADED_TILTING_THRUST_PAD = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.FluidFilm", "LoadedTiltingThrustPad"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadedTiltingThrustPad")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedTiltingThrustPad._Cast_LoadedTiltingThrustPad"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedTiltingThrustPad",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedTiltingThrustPad:
    """Special nested class for casting LoadedTiltingThrustPad to subclasses."""

    __parent__: "LoadedTiltingThrustPad"

    @property
    def loaded_fluid_film_bearing_pad(
        self: "CastSelf",
    ) -> "_2328.LoadedFluidFilmBearingPad":
        return self.__parent__._cast(_2328.LoadedFluidFilmBearingPad)

    @property
    def loaded_tilting_thrust_pad(self: "CastSelf") -> "LoadedTiltingThrustPad":
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
class LoadedTiltingThrustPad(_2328.LoadedFluidFilmBearingPad):
    """LoadedTiltingThrustPad

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_TILTING_THRUST_PAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def effective_film_kinematic_viscosity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveFilmKinematicViscosity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def effective_film_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EffectiveFilmTemperature")

        if temp is None:
            return 0.0

        return temp

    @effective_film_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def effective_film_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EffectiveFilmTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def film_thickness_minimum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FilmThicknessMinimum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def film_thickness_at_pivot(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FilmThicknessAtPivot")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Force")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_flow_at_leading_edge(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantFlowAtLeadingEdge")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_flow_at_trailing_edge(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantFlowAtTrailingEdge")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_side_flow(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantSideFlow")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_temperature_at_leading_edge(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantTemperatureAtLeadingEdge")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_temperature_at_trailing_edge(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LubricantTemperatureAtTrailingEdge"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pressure_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reynolds_number(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReynoldsNumber")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tilt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Tilt")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedTiltingThrustPad":
        """Cast to another type.

        Returns:
            _Cast_LoadedTiltingThrustPad
        """
        return _Cast_LoadedTiltingThrustPad(self)
