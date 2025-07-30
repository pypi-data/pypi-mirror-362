"""WindTurbineSingleBladeDetails"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_WIND_TURBINE_SINGLE_BLADE_DETAILS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "WindTurbineSingleBladeDetails"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model import _2712

    Self = TypeVar("Self", bound="WindTurbineSingleBladeDetails")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WindTurbineSingleBladeDetails._Cast_WindTurbineSingleBladeDetails",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WindTurbineSingleBladeDetails",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WindTurbineSingleBladeDetails:
    """Special nested class for casting WindTurbineSingleBladeDetails to subclasses."""

    __parent__: "WindTurbineSingleBladeDetails"

    @property
    def wind_turbine_single_blade_details(
        self: "CastSelf",
    ) -> "WindTurbineSingleBladeDetails":
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
class WindTurbineSingleBladeDetails(_0.APIBase):
    """WindTurbineSingleBladeDetails

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WIND_TURBINE_SINGLE_BLADE_DETAILS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def blade_drawing_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BladeDrawingLength")

        if temp is None:
            return 0.0

        return temp

    @blade_drawing_length.setter
    @exception_bridge
    @enforce_parameter_types
    def blade_drawing_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BladeDrawingLength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def blade_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BladeLength")

        if temp is None:
            return 0.0

        return temp

    @blade_length.setter
    @exception_bridge
    @enforce_parameter_types
    def blade_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BladeLength", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def blade_mass(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BladeMass")

        if temp is None:
            return 0.0

        return temp

    @blade_mass.setter
    @exception_bridge
    @enforce_parameter_types
    def blade_mass(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BladeMass", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def mass_moment_of_inertia_about_hub(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MassMomentOfInertiaAboutHub")

        if temp is None:
            return 0.0

        return temp

    @mass_moment_of_inertia_about_hub.setter
    @exception_bridge
    @enforce_parameter_types
    def mass_moment_of_inertia_about_hub(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MassMomentOfInertiaAboutHub",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def scale_blade_drawing_to_blade_drawing_length(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ScaleBladeDrawingToBladeDrawingLength"
        )

        if temp is None:
            return False

        return temp

    @scale_blade_drawing_to_blade_drawing_length.setter
    @exception_bridge
    @enforce_parameter_types
    def scale_blade_drawing_to_blade_drawing_length(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ScaleBladeDrawingToBladeDrawingLength",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def edgewise_modes(self: "Self") -> "_2712.WindTurbineBladeModeDetails":
        """mastapy.system_model.part_model.WindTurbineBladeModeDetails

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EdgewiseModes")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def flapwise_modes(self: "Self") -> "_2712.WindTurbineBladeModeDetails":
        """mastapy.system_model.part_model.WindTurbineBladeModeDetails

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlapwiseModes")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_WindTurbineSingleBladeDetails":
        """Cast to another type.

        Returns:
            _Cast_WindTurbineSingleBladeDetails
        """
        return _Cast_WindTurbineSingleBladeDetails(self)
