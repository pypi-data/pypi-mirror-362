"""ISO153122018Results"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_ISO153122018_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "ISO153122018Results"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ISO153122018Results")
    CastSelf = TypeVar(
        "CastSelf", bound="ISO153122018Results._Cast_ISO153122018Results"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO153122018Results",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO153122018Results:
    """Special nested class for casting ISO153122018Results to subclasses."""

    __parent__: "ISO153122018Results"

    @property
    def iso153122018_results(self: "CastSelf") -> "ISO153122018Results":
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
class ISO153122018Results(_0.APIBase):
    """ISO153122018Results

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO153122018_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def coefficient_for_the_load_dependent_friction_moment_for_the_reference_conditions(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "CoefficientForTheLoadDependentFrictionMomentForTheReferenceConditions",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def coefficient_for_the_load_independent_friction_moment_for_the_reference_conditions(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "CoefficientForTheLoadIndependentFrictionMomentForTheReferenceConditions",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def heat_emitting_reference_surface_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeatEmittingReferenceSurfaceArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_dependent_frictional_moment_under_reference_conditions_at_the_thermal_speed_rating(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LoadDependentFrictionalMomentUnderReferenceConditionsAtTheThermalSpeedRating",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_independent_frictional_moment_under_reference_conditions_at_the_thermal_speed_rating(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LoadIndependentFrictionalMomentUnderReferenceConditionsAtTheThermalSpeedRating",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_under_reference_conditions_at_the_thermal_speed_rating(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossUnderReferenceConditionsAtTheThermalSpeedRating"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reason_for_invalidity(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReasonForInvalidity")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def reference_heat_flow(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceHeatFlow")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reference_heat_flow_density(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceHeatFlowDensity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reference_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def thermal_speed_rating(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalSpeedRating")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def viscosity_of_reference_oil(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ViscosityOfReferenceOil")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO153122018Results":
        """Cast to another type.

        Returns:
            _Cast_ISO153122018Results
        """
        return _Cast_ISO153122018Results(self)
