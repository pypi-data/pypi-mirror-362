"""FESubstructureWithSelectionForHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.fe import _2612

_FE_SUBSTRUCTURE_WITH_SELECTION_FOR_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FESubstructureWithSelectionForHarmonicAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis.dev_tools_analyses import _271
    from mastapy._private.system_model.fe import _2581, _2625

    Self = TypeVar("Self", bound="FESubstructureWithSelectionForHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FESubstructureWithSelectionForHarmonicAnalysis._Cast_FESubstructureWithSelectionForHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FESubstructureWithSelectionForHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESubstructureWithSelectionForHarmonicAnalysis:
    """Special nested class for casting FESubstructureWithSelectionForHarmonicAnalysis to subclasses."""

    __parent__: "FESubstructureWithSelectionForHarmonicAnalysis"

    @property
    def fe_substructure_with_selection(
        self: "CastSelf",
    ) -> "_2612.FESubstructureWithSelection":
        return self.__parent__._cast(_2612.FESubstructureWithSelection)

    @property
    def base_fe_with_selection(self: "CastSelf") -> "_2581.BaseFEWithSelection":
        from mastapy._private.system_model.fe import _2581

        return self.__parent__._cast(_2581.BaseFEWithSelection)

    @property
    def fe_substructure_with_selection_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "FESubstructureWithSelectionForHarmonicAnalysis":
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
class FESubstructureWithSelectionForHarmonicAnalysis(_2612.FESubstructureWithSelection):
    """FESubstructureWithSelectionForHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SUBSTRUCTURE_WITH_SELECTION_FOR_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def alpha_damping_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AlphaDampingValue")

        if temp is None:
            return 0.0

        return temp

    @alpha_damping_value.setter
    @exception_bridge
    @enforce_parameter_types
    def alpha_damping_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AlphaDampingValue",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def beta_damping_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BetaDampingValue")

        if temp is None:
            return 0.0

        return temp

    @beta_damping_value.setter
    @exception_bridge
    @enforce_parameter_types
    def beta_damping_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BetaDampingValue", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def frequency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Frequency")

        if temp is None:
            return 0.0

        return temp

    @frequency.setter
    @exception_bridge
    @enforce_parameter_types
    def frequency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Frequency", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def harmonic_draw_style(self: "Self") -> "_271.FEModelHarmonicAnalysisDrawStyle":
        """mastapy.nodal_analysis.dev_tools_analyses.FEModelHarmonicAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def boundary_conditions_all_nodes(
        self: "Self",
    ) -> "List[_2625.NodeBoundaryConditionStaticAnalysis]":
        """List[mastapy.system_model.fe.NodeBoundaryConditionStaticAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoundaryConditionsAllNodes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def export_velocity_to_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ExportVelocityToFile")

    @exception_bridge
    def solve_for_current_inputs(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SolveForCurrentInputs")

    @property
    def cast_to(self: "Self") -> "_Cast_FESubstructureWithSelectionForHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_FESubstructureWithSelectionForHarmonicAnalysis
        """
        return _Cast_FESubstructureWithSelectionForHarmonicAnalysis(self)
