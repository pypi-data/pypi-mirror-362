"""FESubstructureWithSelectionForStaticAnalysis"""

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
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.fe import _2612
from mastapy._private.utility.enums import _2019

_FE_SUBSTRUCTURE_WITH_SELECTION_FOR_STATIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FESubstructureWithSelectionForStaticAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1748
    from mastapy._private.nodal_analysis.component_mode_synthesis import _322
    from mastapy._private.nodal_analysis.dev_tools_analyses import _276
    from mastapy._private.system_model.fe import _2581, _2625

    Self = TypeVar("Self", bound="FESubstructureWithSelectionForStaticAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FESubstructureWithSelectionForStaticAnalysis._Cast_FESubstructureWithSelectionForStaticAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FESubstructureWithSelectionForStaticAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESubstructureWithSelectionForStaticAnalysis:
    """Special nested class for casting FESubstructureWithSelectionForStaticAnalysis to subclasses."""

    __parent__: "FESubstructureWithSelectionForStaticAnalysis"

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
    def fe_substructure_with_selection_for_static_analysis(
        self: "CastSelf",
    ) -> "FESubstructureWithSelectionForStaticAnalysis":
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
class FESubstructureWithSelectionForStaticAnalysis(_2612.FESubstructureWithSelection):
    """FESubstructureWithSelectionForStaticAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SUBSTRUCTURE_WITH_SELECTION_FOR_STATIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def average_stress_to_nodes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "AverageStressToNodes")

        if temp is None:
            return False

        return temp

    @average_stress_to_nodes.setter
    @exception_bridge
    @enforce_parameter_types
    def average_stress_to_nodes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AverageStressToNodes",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def contour_option(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption":
        """EnumWithSelectedValue[mastapy.utility.enums.ThreeDViewContourOption]"""
        temp = pythonnet_property_get(self.wrapped, "ContourOption")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @contour_option.setter
    @exception_bridge
    @enforce_parameter_types
    def contour_option(self: "Self", value: "_2019.ThreeDViewContourOption") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ContourOption", value)

    @property
    @exception_bridge
    def temperature_change_from_nominal(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TemperatureChangeFromNominal")

        if temp is None:
            return 0.0

        return temp

    @temperature_change_from_nominal.setter
    @exception_bridge
    @enforce_parameter_types
    def temperature_change_from_nominal(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TemperatureChangeFromNominal",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def full_fe_results(self: "Self") -> "_322.StaticCMSResults":
        """mastapy.nodal_analysis.component_mode_synthesis.StaticCMSResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullFEResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def static_draw_style(self: "Self") -> "_276.FEModelStaticAnalysisDrawStyle":
        """mastapy.nodal_analysis.dev_tools_analyses.FEModelStaticAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticDrawStyle")

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

    @property
    @exception_bridge
    def boundary_conditions_selected_nodes(
        self: "Self",
    ) -> "List[_2625.NodeBoundaryConditionStaticAnalysis]":
        """List[mastapy.system_model.fe.NodeBoundaryConditionStaticAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoundaryConditionsSelectedNodes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def displacement_results(
        self: "Self",
    ) -> "List[_1748.VectorWithLinearAndAngularComponents]":
        """List[mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DisplacementResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def force_results(
        self: "Self",
    ) -> "List[_1748.VectorWithLinearAndAngularComponents]":
        """List[mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def reset_displacements(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ResetDisplacements")

    @exception_bridge
    def reset_forces(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ResetForces")

    @exception_bridge
    def solve(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Solve")

    @exception_bridge
    def torque_transfer_check(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "TorqueTransferCheck")

    @property
    def cast_to(self: "Self") -> "_Cast_FESubstructureWithSelectionForStaticAnalysis":
        """Cast to another type.

        Returns:
            _Cast_FESubstructureWithSelectionForStaticAnalysis
        """
        return _Cast_FESubstructureWithSelectionForStaticAnalysis(self)
