"""MaterialPropertiesReporting"""

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
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.fe_tools.enums import _1364

_MATERIAL_PROPERTIES_REPORTING = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "MaterialPropertiesReporting",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _292,
        _305,
        _307,
        _308,
    )

    Self = TypeVar("Self", bound="MaterialPropertiesReporting")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MaterialPropertiesReporting._Cast_MaterialPropertiesReporting",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MaterialPropertiesReporting",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MaterialPropertiesReporting:
    """Special nested class for casting MaterialPropertiesReporting to subclasses."""

    __parent__: "MaterialPropertiesReporting"

    @property
    def material_properties_reporting(
        self: "CastSelf",
    ) -> "MaterialPropertiesReporting":
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
class MaterialPropertiesReporting(_0.APIBase):
    """MaterialPropertiesReporting

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MATERIAL_PROPERTIES_REPORTING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def class_(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_MaterialPropertyClass":
        """EnumWithSelectedValue[mastapy.fe_tools.enums.MaterialPropertyClass]"""
        temp = pythonnet_property_get(self.wrapped, "Class")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_MaterialPropertyClass.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @class_.setter
    @exception_bridge
    @enforce_parameter_types
    def class_(self: "Self", value: "_1364.MaterialPropertyClass") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MaterialPropertyClass.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Class", value)

    @property
    @exception_bridge
    def density(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Density")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @density.setter
    @exception_bridge
    @enforce_parameter_types
    def density(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Density", value)

    @property
    @exception_bridge
    def id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ID")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def modulus_of_elasticity(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ModulusOfElasticity")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @modulus_of_elasticity.setter
    @exception_bridge
    @enforce_parameter_types
    def modulus_of_elasticity(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ModulusOfElasticity", value)

    @property
    @exception_bridge
    def poissons_ratio(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PoissonsRatio")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @poissons_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def poissons_ratio(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PoissonsRatio", value)

    @property
    @exception_bridge
    def thermal_expansion_coefficient(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ThermalExpansionCoefficient")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @thermal_expansion_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def thermal_expansion_coefficient(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ThermalExpansionCoefficient", value)

    @property
    @exception_bridge
    def elastic_modulus_components(
        self: "Self",
    ) -> "_292.ElasticModulusOrthotropicComponents":
        """mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElasticModulusOrthotropicComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticModulusComponents")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def poissons_ratio_components(
        self: "Self",
    ) -> "_305.PoissonRatioOrthotropicComponents":
        """mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.PoissonRatioOrthotropicComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PoissonsRatioComponents")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shear_modulus_components(
        self: "Self",
    ) -> "_307.ShearModulusOrthotropicComponents":
        """mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ShearModulusOrthotropicComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearModulusComponents")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def thermal_expansion_coefficient_components(
        self: "Self",
    ) -> "_308.ThermalExpansionOrthotropicComponents":
        """mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ThermalExpansionOrthotropicComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThermalExpansionCoefficientComponents"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def elastic_stiffness_tensor_lower_triangle(self: "Self") -> "List[float]":
        """List[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "ElasticStiffnessTensorLowerTriangle"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @elastic_stiffness_tensor_lower_triangle.setter
    @exception_bridge
    @enforce_parameter_types
    def elastic_stiffness_tensor_lower_triangle(
        self: "Self", value: "List[float]"
    ) -> None:
        value = conversion.mp_to_pn_objects_in_list(value)
        pythonnet_property_set(
            self.wrapped, "ElasticStiffnessTensorLowerTriangle", value
        )

    @property
    @exception_bridge
    def thermal_expansion_coefficient_vector(self: "Self") -> "List[float]":
        """List[float]"""
        temp = pythonnet_property_get(self.wrapped, "ThermalExpansionCoefficientVector")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @thermal_expansion_coefficient_vector.setter
    @exception_bridge
    @enforce_parameter_types
    def thermal_expansion_coefficient_vector(
        self: "Self", value: "List[float]"
    ) -> None:
        value = conversion.mp_to_pn_objects_in_list(value)
        pythonnet_property_set(self.wrapped, "ThermalExpansionCoefficientVector", value)

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
    def cast_to(self: "Self") -> "_Cast_MaterialPropertiesReporting":
        """Cast to another type.

        Returns:
            _Cast_MaterialPropertiesReporting
        """
        return _Cast_MaterialPropertiesReporting(self)
