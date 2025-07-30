"""PointLoadLoadCase"""

from __future__ import annotations

from enum import Enum
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
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7853

_POINT_LOAD_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PointLoadLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.nodal_analysis.varying_input_components import _101, _102
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7706,
        _7795,
        _7799,
        _7808,
    )
    from mastapy._private.system_model.part_model import _2702

    Self = TypeVar("Self", bound="PointLoadLoadCase")
    CastSelf = TypeVar("CastSelf", bound="PointLoadLoadCase._Cast_PointLoadLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("PointLoadLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PointLoadLoadCase:
    """Special nested class for casting PointLoadLoadCase to subclasses."""

    __parent__: "PointLoadLoadCase"

    @property
    def virtual_component_load_case(
        self: "CastSelf",
    ) -> "_7853.VirtualComponentLoadCase":
        return self.__parent__._cast(_7853.VirtualComponentLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7795.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7795,
        )

        return self.__parent__._cast(_7795.MountableComponentLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_7706.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7706,
        )

        return self.__parent__._cast(_7706.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7799.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7799,
        )

        return self.__parent__._cast(_7799.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def point_load_load_case(self: "CastSelf") -> "PointLoadLoadCase":
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
class PointLoadLoadCase(_7853.VirtualComponentLoadCase):
    """PointLoadLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POINT_LOAD_LOAD_CASE

    class ForceSpecification(Enum):
        """ForceSpecification is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _POINT_LOAD_LOAD_CASE.ForceSpecification

        RADIAL_TANGENTIAL = 0
        FORCE_X_FORCE_Y = 1

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    ForceSpecification.__setattr__ = __enum_setattr
    ForceSpecification.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle_of_radial_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngleOfRadialForce")

        if temp is None:
            return 0.0

        return temp

    @angle_of_radial_force.setter
    @exception_bridge
    @enforce_parameter_types
    def angle_of_radial_force(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AngleOfRadialForce",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def displacement_x(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DisplacementX")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @displacement_x.setter
    @exception_bridge
    @enforce_parameter_types
    def displacement_x(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DisplacementX", value)

    @property
    @exception_bridge
    def displacement_y(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DisplacementY")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @displacement_y.setter
    @exception_bridge
    @enforce_parameter_types
    def displacement_y(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DisplacementY", value)

    @property
    @exception_bridge
    def displacement_z(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DisplacementZ")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @displacement_z.setter
    @exception_bridge
    @enforce_parameter_types
    def displacement_z(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DisplacementZ", value)

    @property
    @exception_bridge
    def force_specification_options(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase.ForceSpecification]"""
        temp = pythonnet_property_get(self.wrapped, "ForceSpecificationOptions")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @force_specification_options.setter
    @exception_bridge
    @enforce_parameter_types
    def force_specification_options(
        self: "Self", value: "PointLoadLoadCase.ForceSpecification"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ForceSpecificationOptions", value)

    @property
    @exception_bridge
    def magnitude_radial_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MagnitudeRadialForce")

        if temp is None:
            return 0.0

        return temp

    @magnitude_radial_force.setter
    @exception_bridge
    @enforce_parameter_types
    def magnitude_radial_force(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MagnitudeRadialForce",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def radial_load(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialLoad")

        if temp is None:
            return 0.0

        return temp

    @radial_load.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_load(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialLoad", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tangential_load(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TangentialLoad")

        if temp is None:
            return 0.0

        return temp

    @tangential_load.setter
    @exception_bridge
    @enforce_parameter_types
    def tangential_load(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TangentialLoad", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def twist_theta_x(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TwistThetaX")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @twist_theta_x.setter
    @exception_bridge
    @enforce_parameter_types
    def twist_theta_x(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TwistThetaX", value)

    @property
    @exception_bridge
    def twist_theta_y(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TwistThetaY")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @twist_theta_y.setter
    @exception_bridge
    @enforce_parameter_types
    def twist_theta_y(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TwistThetaY", value)

    @property
    @exception_bridge
    def twist_theta_z(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TwistThetaZ")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @twist_theta_z.setter
    @exception_bridge
    @enforce_parameter_types
    def twist_theta_z(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TwistThetaZ", value)

    @property
    @exception_bridge
    def axial_load(self: "Self") -> "_101.ForceInputComponent":
        """mastapy.nodal_analysis.varying_input_components.ForceInputComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialLoad")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2702.PointLoad":
        """mastapy.system_model.part_model.PointLoad

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def force_x(self: "Self") -> "_101.ForceInputComponent":
        """mastapy.nodal_analysis.varying_input_components.ForceInputComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceX")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def force_y(self: "Self") -> "_101.ForceInputComponent":
        """mastapy.nodal_analysis.varying_input_components.ForceInputComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceY")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def moment_x(self: "Self") -> "_102.MomentInputComponent":
        """mastapy.nodal_analysis.varying_input_components.MomentInputComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MomentX")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def moment_y(self: "Self") -> "_102.MomentInputComponent":
        """mastapy.nodal_analysis.varying_input_components.MomentInputComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MomentY")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def moment_z(self: "Self") -> "_102.MomentInputComponent":
        """mastapy.nodal_analysis.varying_input_components.MomentInputComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MomentZ")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def get_harmonic_load_data_for_import(
        self: "Self",
    ) -> "_7808.PointLoadHarmonicLoadData":
        """mastapy.system_model.analyses_and_results.static_loads.PointLoadHarmonicLoadData"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetHarmonicLoadDataForImport"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PointLoadLoadCase":
        """Cast to another type.

        Returns:
            _Cast_PointLoadLoadCase
        """
        return _Cast_PointLoadLoadCase(self)
