"""TESetUpForDynamicAnalysisOptions"""

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

_TE_SET_UP_FOR_DYNAMIC_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "TESetUpForDynamicAnalysisOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TESetUpForDynamicAnalysisOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TESetUpForDynamicAnalysisOptions._Cast_TESetUpForDynamicAnalysisOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TESetUpForDynamicAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TESetUpForDynamicAnalysisOptions:
    """Special nested class for casting TESetUpForDynamicAnalysisOptions to subclasses."""

    __parent__: "TESetUpForDynamicAnalysisOptions"

    @property
    def te_set_up_for_dynamic_analysis_options(
        self: "CastSelf",
    ) -> "TESetUpForDynamicAnalysisOptions":
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
class TESetUpForDynamicAnalysisOptions(_0.APIBase):
    """TESetUpForDynamicAnalysisOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TE_SET_UP_FOR_DYNAMIC_ANALYSIS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def include_misalignment_excitation(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeMisalignmentExcitation")

        if temp is None:
            return False

        return temp

    @include_misalignment_excitation.setter
    @exception_bridge
    @enforce_parameter_types
    def include_misalignment_excitation(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeMisalignmentExcitation",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_data_logger_for_advanced_system_deflection_single_tooth_pass_harmonic_excitation_type_options(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "UseDataLoggerForAdvancedSystemDeflectionSingleToothPassHarmonicExcitationTypeOptions",
        )

        if temp is None:
            return False

        return temp

    @use_data_logger_for_advanced_system_deflection_single_tooth_pass_harmonic_excitation_type_options.setter
    @exception_bridge
    @enforce_parameter_types
    def use_data_logger_for_advanced_system_deflection_single_tooth_pass_harmonic_excitation_type_options(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDataLoggerForAdvancedSystemDeflectionSingleToothPassHarmonicExcitationTypeOptions",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TESetUpForDynamicAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_TESetUpForDynamicAnalysisOptions
        """
        return _Cast_TESetUpForDynamicAnalysisOptions(self)
