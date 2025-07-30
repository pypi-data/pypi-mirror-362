"""LoadedNeedleRollerBearingElement"""

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
from mastapy._private.bearings.bearing_results.rolling import _2216

_LOADED_NEEDLE_ROLLER_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedNeedleRollerBearingElement"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2222, _2235, _2236

    Self = TypeVar("Self", bound="LoadedNeedleRollerBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedNeedleRollerBearingElement._Cast_LoadedNeedleRollerBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedNeedleRollerBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedNeedleRollerBearingElement:
    """Special nested class for casting LoadedNeedleRollerBearingElement to subclasses."""

    __parent__: "LoadedNeedleRollerBearingElement"

    @property
    def loaded_cylindrical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2216.LoadedCylindricalRollerBearingElement":
        return self.__parent__._cast(_2216.LoadedCylindricalRollerBearingElement)

    @property
    def loaded_non_barrel_roller_element(
        self: "CastSelf",
    ) -> "_2235.LoadedNonBarrelRollerElement":
        from mastapy._private.bearings.bearing_results.rolling import _2235

        return self.__parent__._cast(_2235.LoadedNonBarrelRollerElement)

    @property
    def loaded_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2236.LoadedRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2236

        return self.__parent__._cast(_2236.LoadedRollerBearingElement)

    @property
    def loaded_element(self: "CastSelf") -> "_2222.LoadedElement":
        from mastapy._private.bearings.bearing_results.rolling import _2222

        return self.__parent__._cast(_2222.LoadedElement)

    @property
    def loaded_needle_roller_bearing_element(
        self: "CastSelf",
    ) -> "LoadedNeedleRollerBearingElement":
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
class LoadedNeedleRollerBearingElement(_2216.LoadedCylindricalRollerBearingElement):
    """LoadedNeedleRollerBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_NEEDLE_ROLLER_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def sliding_power_loss_from_hysteresis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SlidingPowerLossFromHysteresis")

        if temp is None:
            return 0.0

        return temp

    @sliding_power_loss_from_hysteresis.setter
    @exception_bridge
    @enforce_parameter_types
    def sliding_power_loss_from_hysteresis(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SlidingPowerLossFromHysteresis",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def sliding_power_loss_from_macro_sliding_due_to_roller_skew(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "SlidingPowerLossFromMacroSlidingDueToRollerSkew"
        )

        if temp is None:
            return 0.0

        return temp

    @sliding_power_loss_from_macro_sliding_due_to_roller_skew.setter
    @exception_bridge
    @enforce_parameter_types
    def sliding_power_loss_from_macro_sliding_due_to_roller_skew(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SlidingPowerLossFromMacroSlidingDueToRollerSkew",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def sliding_power_loss_roller_cage_axial_component(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "SlidingPowerLossRollerCageAxialComponent"
        )

        if temp is None:
            return 0.0

        return temp

    @sliding_power_loss_roller_cage_axial_component.setter
    @exception_bridge
    @enforce_parameter_types
    def sliding_power_loss_roller_cage_axial_component(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SlidingPowerLossRollerCageAxialComponent",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def sliding_power_loss_roller_cage_moment_component(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "SlidingPowerLossRollerCageMomentComponent"
        )

        if temp is None:
            return 0.0

        return temp

    @sliding_power_loss_roller_cage_moment_component.setter
    @exception_bridge
    @enforce_parameter_types
    def sliding_power_loss_roller_cage_moment_component(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SlidingPowerLossRollerCageMomentComponent",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def sliding_power_loss_roller_cage_radial_component(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "SlidingPowerLossRollerCageRadialComponent"
        )

        if temp is None:
            return 0.0

        return temp

    @sliding_power_loss_roller_cage_radial_component.setter
    @exception_bridge
    @enforce_parameter_types
    def sliding_power_loss_roller_cage_radial_component(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SlidingPowerLossRollerCageRadialComponent",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedNeedleRollerBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedNeedleRollerBearingElement
        """
        return _Cast_LoadedNeedleRollerBearingElement(self)
