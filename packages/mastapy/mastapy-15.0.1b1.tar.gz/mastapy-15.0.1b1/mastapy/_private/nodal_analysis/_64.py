"""FEMeshingOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_FE_MESHING_OPTIONS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "FEMeshingOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import _1389, _1391, _1392, _1393, _1396
    from mastapy._private.nodal_analysis import _61, _65, _80, _91, _98

    Self = TypeVar("Self", bound="FEMeshingOptions")
    CastSelf = TypeVar("CastSelf", bound="FEMeshingOptions._Cast_FEMeshingOptions")


__docformat__ = "restructuredtext en"
__all__ = ("FEMeshingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEMeshingOptions:
    """Special nested class for casting FEMeshingOptions to subclasses."""

    __parent__: "FEMeshingOptions"

    @property
    def meshing_options(self: "CastSelf") -> "_80.MeshingOptions":
        from mastapy._private.nodal_analysis import _80

        return self.__parent__._cast(_80.MeshingOptions)

    @property
    def shaft_fe_meshing_options(self: "CastSelf") -> "_91.ShaftFEMeshingOptions":
        from mastapy._private.nodal_analysis import _91

        return self.__parent__._cast(_91.ShaftFEMeshingOptions)

    @property
    def electric_machine_electromagnetic_and_thermal_meshing_options(
        self: "CastSelf",
    ) -> "_1389.ElectricMachineElectromagneticAndThermalMeshingOptions":
        from mastapy._private.electric_machines import _1389

        return self.__parent__._cast(
            _1389.ElectricMachineElectromagneticAndThermalMeshingOptions
        )

    @property
    def electric_machine_mechanical_analysis_meshing_options(
        self: "CastSelf",
    ) -> "_1391.ElectricMachineMechanicalAnalysisMeshingOptions":
        from mastapy._private.electric_machines import _1391

        return self.__parent__._cast(
            _1391.ElectricMachineMechanicalAnalysisMeshingOptions
        )

    @property
    def electric_machine_meshing_options(
        self: "CastSelf",
    ) -> "_1392.ElectricMachineMeshingOptions":
        from mastapy._private.electric_machines import _1392

        return self.__parent__._cast(_1392.ElectricMachineMeshingOptions)

    @property
    def electric_machine_meshing_options_base(
        self: "CastSelf",
    ) -> "_1393.ElectricMachineMeshingOptionsBase":
        from mastapy._private.electric_machines import _1393

        return self.__parent__._cast(_1393.ElectricMachineMeshingOptionsBase)

    @property
    def electric_machine_thermal_meshing_options(
        self: "CastSelf",
    ) -> "_1396.ElectricMachineThermalMeshingOptions":
        from mastapy._private.electric_machines import _1396

        return self.__parent__._cast(_1396.ElectricMachineThermalMeshingOptions)

    @property
    def fe_meshing_options(self: "CastSelf") -> "FEMeshingOptions":
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
class FEMeshingOptions(_0.APIBase):
    """FEMeshingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_MESHING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def element_order(self: "Self") -> "_61.ElementOrder":
        """mastapy.nodal_analysis.ElementOrder"""
        temp = pythonnet_property_get(self.wrapped, "ElementOrder")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.ElementOrder"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._61", "ElementOrder"
        )(value)

    @element_order.setter
    @exception_bridge
    @enforce_parameter_types
    def element_order(self: "Self", value: "_61.ElementOrder") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.ElementOrder"
        )
        pythonnet_property_set(self.wrapped, "ElementOrder", value)

    @property
    @exception_bridge
    def element_shape(self: "Self") -> "_98.VolumeElementShape":
        """mastapy.nodal_analysis.VolumeElementShape"""
        temp = pythonnet_property_get(self.wrapped, "ElementShape")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.VolumeElementShape"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._98", "VolumeElementShape"
        )(value)

    @element_shape.setter
    @exception_bridge
    @enforce_parameter_types
    def element_shape(self: "Self", value: "_98.VolumeElementShape") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.VolumeElementShape"
        )
        pythonnet_property_set(self.wrapped, "ElementShape", value)

    @property
    @exception_bridge
    def maximum_chord_height(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumChordHeight")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_chord_height.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_chord_height(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumChordHeight", value)

    @property
    @exception_bridge
    def maximum_edge_altitude_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumEdgeAltitudeRatio")

        if temp is None:
            return 0.0

        return temp

    @maximum_edge_altitude_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_edge_altitude_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumEdgeAltitudeRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_growth_rate(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumGrowthRate")

        if temp is None:
            return 0.0

        return temp

    @maximum_growth_rate.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_growth_rate(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumGrowthRate",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_spanning_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumSpanningAngle")

        if temp is None:
            return 0.0

        return temp

    @maximum_spanning_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_spanning_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumSpanningAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_element_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumElementSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_element_size.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_element_size(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumElementSize", value)

    @property
    @exception_bridge
    def minimum_triangle_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumTriangleAngle")

        if temp is None:
            return 0.0

        return temp

    @minimum_triangle_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_triangle_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumTriangleAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def preserve_edge_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PreserveEdgeAngle")

        if temp is None:
            return 0.0

        return temp

    @preserve_edge_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def preserve_edge_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PreserveEdgeAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def preserve_node_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PreserveNodeAngle")

        if temp is None:
            return 0.0

        return temp

    @preserve_node_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def preserve_node_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PreserveNodeAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def meshing_problems(self: "Self") -> "List[_65.FEMeshingProblem]":
        """List[mastapy.nodal_analysis.FEMeshingProblem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshingProblems")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def cast_to(self: "Self") -> "_Cast_FEMeshingOptions":
        """Cast to another type.

        Returns:
            _Cast_FEMeshingOptions
        """
        return _Cast_FEMeshingOptions(self)
