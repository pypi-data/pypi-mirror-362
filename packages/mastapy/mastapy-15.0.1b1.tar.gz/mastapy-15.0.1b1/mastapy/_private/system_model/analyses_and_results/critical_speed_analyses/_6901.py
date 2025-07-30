"""CriticalSpeedAnalysisOptions"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CRITICAL_SPEED_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "CriticalSpeedAnalysisOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CriticalSpeedAnalysisOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CriticalSpeedAnalysisOptions._Cast_CriticalSpeedAnalysisOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CriticalSpeedAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CriticalSpeedAnalysisOptions:
    """Special nested class for casting CriticalSpeedAnalysisOptions to subclasses."""

    __parent__: "CriticalSpeedAnalysisOptions"

    @property
    def critical_speed_analysis_options(
        self: "CastSelf",
    ) -> "CriticalSpeedAnalysisOptions":
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
class CriticalSpeedAnalysisOptions(_0.APIBase):
    """CriticalSpeedAnalysisOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CRITICAL_SPEED_ANALYSIS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialStiffness")

        if temp is None:
            return 0.0

        return temp

    @axial_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AxialStiffness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def final_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FinalStiffness")

        if temp is None:
            return 0.0

        return temp

    @final_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def final_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FinalStiffness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def include_damping_effects(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeDampingEffects")

        if temp is None:
            return False

        return temp

    @include_damping_effects.setter
    @exception_bridge
    @enforce_parameter_types
    def include_damping_effects(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeDampingEffects",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_gyroscopic_effects(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeGyroscopicEffects")

        if temp is None:
            return False

        return temp

    @include_gyroscopic_effects.setter
    @exception_bridge
    @enforce_parameter_types
    def include_gyroscopic_effects(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeGyroscopicEffects",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def initial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InitialStiffness")

        if temp is None:
            return 0.0

        return temp

    @initial_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def initial_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "InitialStiffness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def number_of_modes(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfModes")

        if temp is None:
            return 0

        return temp

    @number_of_modes.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_modes(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfModes", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_stiffnesses(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfStiffnesses")

        if temp is None:
            return 0

        return temp

    @number_of_stiffnesses.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_stiffnesses(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfStiffnesses", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def sort_modes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SortModes")

        if temp is None:
            return False

        return temp

    @sort_modes.setter
    @exception_bridge
    @enforce_parameter_types
    def sort_modes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SortModes", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def tilt_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltStiffness")

        if temp is None:
            return 0.0

        return temp

    @tilt_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltStiffness", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CriticalSpeedAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_CriticalSpeedAnalysisOptions
        """
        return _Cast_CriticalSpeedAnalysisOptions(self)
