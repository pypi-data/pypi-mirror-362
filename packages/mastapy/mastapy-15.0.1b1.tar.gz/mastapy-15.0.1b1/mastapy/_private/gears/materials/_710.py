"""ScriptCoefficientOfFrictionCalculator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.materials import _691

_SCRIPT_COEFFICIENT_OF_FRICTION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "ScriptCoefficientOfFrictionCalculator"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.materials import _681

    Self = TypeVar("Self", bound="ScriptCoefficientOfFrictionCalculator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ScriptCoefficientOfFrictionCalculator._Cast_ScriptCoefficientOfFrictionCalculator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ScriptCoefficientOfFrictionCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ScriptCoefficientOfFrictionCalculator:
    """Special nested class for casting ScriptCoefficientOfFrictionCalculator to subclasses."""

    __parent__: "ScriptCoefficientOfFrictionCalculator"

    @property
    def instantaneous_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_691.InstantaneousCoefficientOfFrictionCalculator":
        return self.__parent__._cast(_691.InstantaneousCoefficientOfFrictionCalculator)

    @property
    def coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_681.CoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _681

        return self.__parent__._cast(_681.CoefficientOfFrictionCalculator)

    @property
    def script_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "ScriptCoefficientOfFrictionCalculator":
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
class ScriptCoefficientOfFrictionCalculator(
    _691.InstantaneousCoefficientOfFrictionCalculator
):
    """ScriptCoefficientOfFrictionCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SCRIPT_COEFFICIENT_OF_FRICTION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def combined_radius_of_curvature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CombinedRadiusOfCurvature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_viscosity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicViscosity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def entrainment_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EntrainmentVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def internal_external_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InternalExternalFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def kinematic_viscosity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KinematicViscosity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_tooth_passing_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionToothPassingSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def roll_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_tooth_passing_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelToothPassingSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ScriptCoefficientOfFrictionCalculator":
        """Cast to another type.

        Returns:
            _Cast_ScriptCoefficientOfFrictionCalculator
        """
        return _Cast_ScriptCoefficientOfFrictionCalculator(self)
