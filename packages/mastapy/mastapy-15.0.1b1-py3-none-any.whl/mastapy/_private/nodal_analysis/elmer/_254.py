"""ElmerResultsViewable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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
from mastapy._private.math_utility import _1711
from mastapy._private.nodal_analysis.elmer import _255

_ELMER_RESULTS_VIEWABLE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.Elmer", "ElmerResultsViewable"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.results import _1509, _1521
    from mastapy._private.nodal_analysis.elmer import _250, _258
    from mastapy._private.utility_gui import _2054

    Self = TypeVar("Self", bound="ElmerResultsViewable")
    CastSelf = TypeVar(
        "CastSelf", bound="ElmerResultsViewable._Cast_ElmerResultsViewable"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElmerResultsViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElmerResultsViewable:
    """Special nested class for casting ElmerResultsViewable to subclasses."""

    __parent__: "ElmerResultsViewable"

    @property
    def electric_machine_mechanical_results_viewable(
        self: "CastSelf",
    ) -> "_1509.ElectricMachineMechanicalResultsViewable":
        from mastapy._private.electric_machines.results import _1509

        return self.__parent__._cast(_1509.ElectricMachineMechanicalResultsViewable)

    @property
    def electric_machine_results_viewable(
        self: "CastSelf",
    ) -> "_1521.ElectricMachineResultsViewable":
        from mastapy._private.electric_machines.results import _1521

        return self.__parent__._cast(_1521.ElectricMachineResultsViewable)

    @property
    def elmer_results_viewable(self: "CastSelf") -> "ElmerResultsViewable":
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
class ElmerResultsViewable(_0.APIBase):
    """ElmerResultsViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELMER_RESULTS_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def current_index(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "CurrentIndex")

        if temp is None:
            return 0

        return temp

    @current_index.setter
    @exception_bridge
    @enforce_parameter_types
    def current_index(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "CurrentIndex", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def degree_of_freedom(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ResultOptionsFor3DVector":
        """EnumWithSelectedValue[mastapy.math_utility.ResultOptionsFor3DVector]"""
        temp = pythonnet_property_get(self.wrapped, "DegreeOfFreedom")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ResultOptionsFor3DVector.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @degree_of_freedom.setter
    @exception_bridge
    @enforce_parameter_types
    def degree_of_freedom(
        self: "Self", value: "_1711.ResultOptionsFor3DVector"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ResultOptionsFor3DVector.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DegreeOfFreedom", value)

    @property
    @exception_bridge
    def elemental_or_nodal_data(self: "Self") -> "_250.ElmerResultEntityType":
        """mastapy.nodal_analysis.elmer.ElmerResultEntityType"""
        temp = pythonnet_property_get(self.wrapped, "ElementalOrNodalData")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.Elmer.ElmerResultEntityType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis.elmer._250", "ElmerResultEntityType"
        )(value)

    @elemental_or_nodal_data.setter
    @exception_bridge
    @enforce_parameter_types
    def elemental_or_nodal_data(
        self: "Self", value: "_250.ElmerResultEntityType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.Elmer.ElmerResultEntityType"
        )
        pythonnet_property_set(self.wrapped, "ElementalOrNodalData", value)

    @property
    @exception_bridge
    def nodal_average_type(self: "Self") -> "_258.NodalAverageType":
        """mastapy.nodal_analysis.elmer.NodalAverageType"""
        temp = pythonnet_property_get(self.wrapped, "NodalAverageType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.Elmer.NodalAverageType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis.elmer._258", "NodalAverageType"
        )(value)

    @nodal_average_type.setter
    @exception_bridge
    @enforce_parameter_types
    def nodal_average_type(self: "Self", value: "_258.NodalAverageType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.Elmer.NodalAverageType"
        )
        pythonnet_property_set(self.wrapped, "NodalAverageType", value)

    @property
    @exception_bridge
    def result_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ElmerResultType":
        """EnumWithSelectedValue[mastapy.nodal_analysis.elmer.ElmerResultType]"""
        temp = pythonnet_property_get(self.wrapped, "ResultType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ElmerResultType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @result_type.setter
    @exception_bridge
    @enforce_parameter_types
    def result_type(self: "Self", value: "_255.ElmerResultType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ElmerResultType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ResultType", value)

    @property
    @exception_bridge
    def show_contour_range_for_all_parts(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowContourRangeForAllParts")

        if temp is None:
            return False

        return temp

    @show_contour_range_for_all_parts.setter
    @exception_bridge
    @enforce_parameter_types
    def show_contour_range_for_all_parts(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowContourRangeForAllParts",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_contour_range_for_all_steps(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowContourRangeForAllSteps")

        if temp is None:
            return False

        return temp

    @show_contour_range_for_all_steps.setter
    @exception_bridge
    @enforce_parameter_types
    def show_contour_range_for_all_steps(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowContourRangeForAllSteps",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_full_model(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowFullModel")

        if temp is None:
            return False

        return temp

    @show_full_model.setter
    @exception_bridge
    @enforce_parameter_types
    def show_full_model(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowFullModel", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def show_in_3d(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowIn3D")

        if temp is None:
            return False

        return temp

    @show_in_3d.setter
    @exception_bridge
    @enforce_parameter_types
    def show_in_3d(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowIn3D", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def show_mesh(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowMesh")

        if temp is None:
            return False

        return temp

    @show_mesh.setter
    @exception_bridge
    @enforce_parameter_types
    def show_mesh(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowMesh", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def scaling_draw_style(self: "Self") -> "_2054.ScalingDrawStyle":
        """mastapy.utility_gui.ScalingDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScalingDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_ElmerResultsViewable":
        """Cast to another type.

        Returns:
            _Cast_ElmerResultsViewable
        """
        return _Cast_ElmerResultsViewable(self)
