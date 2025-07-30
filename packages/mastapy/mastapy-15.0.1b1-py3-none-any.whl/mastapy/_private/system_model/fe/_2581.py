"""BaseFEWithSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_BASE_FE_WITH_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "BaseFEWithSelection"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.nodal_analysis.dev_tools_analyses import (
        _262,
        _270,
        _278,
        _279,
    )
    from mastapy._private.system_model.fe import (
        _2612,
        _2613,
        _2614,
        _2615,
        _2616,
        _2633,
    )
    from mastapy._private.system_model.part_model import _2670

    Self = TypeVar("Self", bound="BaseFEWithSelection")
    CastSelf = TypeVar(
        "CastSelf", bound="BaseFEWithSelection._Cast_BaseFEWithSelection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BaseFEWithSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BaseFEWithSelection:
    """Special nested class for casting BaseFEWithSelection to subclasses."""

    __parent__: "BaseFEWithSelection"

    @property
    def fe_substructure_with_selection(
        self: "CastSelf",
    ) -> "_2612.FESubstructureWithSelection":
        from mastapy._private.system_model.fe import _2612

        return self.__parent__._cast(_2612.FESubstructureWithSelection)

    @property
    def fe_substructure_with_selection_components(
        self: "CastSelf",
    ) -> "_2613.FESubstructureWithSelectionComponents":
        from mastapy._private.system_model.fe import _2613

        return self.__parent__._cast(_2613.FESubstructureWithSelectionComponents)

    @property
    def fe_substructure_with_selection_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2614.FESubstructureWithSelectionForHarmonicAnalysis":
        from mastapy._private.system_model.fe import _2614

        return self.__parent__._cast(
            _2614.FESubstructureWithSelectionForHarmonicAnalysis
        )

    @property
    def fe_substructure_with_selection_for_modal_analysis(
        self: "CastSelf",
    ) -> "_2615.FESubstructureWithSelectionForModalAnalysis":
        from mastapy._private.system_model.fe import _2615

        return self.__parent__._cast(_2615.FESubstructureWithSelectionForModalAnalysis)

    @property
    def fe_substructure_with_selection_for_static_analysis(
        self: "CastSelf",
    ) -> "_2616.FESubstructureWithSelectionForStaticAnalysis":
        from mastapy._private.system_model.fe import _2616

        return self.__parent__._cast(_2616.FESubstructureWithSelectionForStaticAnalysis)

    @property
    def race_bearing_fe_with_selection(
        self: "CastSelf",
    ) -> "_2633.RaceBearingFEWithSelection":
        from mastapy._private.system_model.fe import _2633

        return self.__parent__._cast(_2633.RaceBearingFEWithSelection)

    @property
    def base_fe_with_selection(self: "CastSelf") -> "BaseFEWithSelection":
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
class BaseFEWithSelection(_0.APIBase):
    """BaseFEWithSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BASE_FE_WITH_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_selected_faces(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfSelectedFaces")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_selected_nodes(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfSelectedNodes")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def selected_component(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedComponent")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def component_draw_style(self: "Self") -> "_270.FEModelComponentDrawStyle":
        """mastapy.nodal_analysis.dev_tools_analyses.FEModelComponentDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def draw_style(self: "Self") -> "_262.DrawStyleForFE":
        """mastapy.nodal_analysis.dev_tools_analyses.DrawStyleForFE

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def node_selection(self: "Self") -> "_279.FENodeSelectionDrawStyle":
        """mastapy.nodal_analysis.dev_tools_analyses.FENodeSelectionDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeSelection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def transparency_draw_style(self: "Self") -> "_278.FEModelTransparencyDrawStyle":
        """mastapy.nodal_analysis.dev_tools_analyses.FEModelTransparencyDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransparencyDrawStyle")

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
    def select_component(self: "Self", component: "_2670.Component") -> None:
        """Method does not return.

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        pythonnet_method_call(
            self.wrapped, "SelectComponent", component.wrapped if component else None
        )

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
    def cast_to(self: "Self") -> "_Cast_BaseFEWithSelection":
        """Cast to another type.

        Returns:
            _Cast_BaseFEWithSelection
        """
        return _Cast_BaseFEWithSelection(self)
