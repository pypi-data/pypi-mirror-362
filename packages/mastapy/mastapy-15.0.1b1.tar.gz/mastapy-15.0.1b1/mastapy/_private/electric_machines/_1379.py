"""CoolingDuctLayerSpecification"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_COOLING_DUCT_LAYER_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "CoolingDuctLayerSpecification"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import _1380

    Self = TypeVar("Self", bound="CoolingDuctLayerSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoolingDuctLayerSpecification._Cast_CoolingDuctLayerSpecification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoolingDuctLayerSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CoolingDuctLayerSpecification:
    """Special nested class for casting CoolingDuctLayerSpecification to subclasses."""

    __parent__: "CoolingDuctLayerSpecification"

    @property
    def cooling_duct_layer_specification(
        self: "CastSelf",
    ) -> "CoolingDuctLayerSpecification":
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
class CoolingDuctLayerSpecification(_0.APIBase):
    """CoolingDuctLayerSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COOLING_DUCT_LAYER_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def corner_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CornerRadius")

        if temp is None:
            return 0.0

        return temp

    @corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def corner_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CornerRadius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def distance_to_lower_arc(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DistanceToLowerArc")

        if temp is None:
            return 0.0

        return temp

    @distance_to_lower_arc.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_to_lower_arc(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceToLowerArc",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def duct_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DuctDiameter")

        if temp is None:
            return 0.0

        return temp

    @duct_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def duct_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DuctDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def first_duct_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstDuctAngle")

        if temp is None:
            return 0.0

        return temp

    @first_duct_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def first_duct_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FirstDuctAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def is_cooling_channel(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsCoolingChannel")

        if temp is None:
            return False

        return temp

    @is_cooling_channel.setter
    @exception_bridge
    @enforce_parameter_types
    def is_cooling_channel(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsCoolingChannel",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def length_in_radial_direction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LengthInRadialDirection")

        if temp is None:
            return 0.0

        return temp

    @length_in_radial_direction.setter
    @exception_bridge
    @enforce_parameter_types
    def length_in_radial_direction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LengthInRadialDirection",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lower_arc_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LowerArcLength")

        if temp is None:
            return 0.0

        return temp

    @lower_arc_length.setter
    @exception_bridge
    @enforce_parameter_types
    def lower_arc_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LowerArcLength", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def lower_fillet_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LowerFilletRadius")

        if temp is None:
            return 0.0

        return temp

    @lower_fillet_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def lower_fillet_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LowerFilletRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def major_axis_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MajorAxisLength")

        if temp is None:
            return 0.0

        return temp

    @major_axis_length.setter
    @exception_bridge
    @enforce_parameter_types
    def major_axis_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MajorAxisLength", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def minor_axis_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinorAxisLength")

        if temp is None:
            return 0.0

        return temp

    @minor_axis_length.setter
    @exception_bridge
    @enforce_parameter_types
    def minor_axis_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MinorAxisLength", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def number_of_ducts(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfDucts")

        if temp is None:
            return 0

        return temp

    @number_of_ducts.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_ducts(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfDucts", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def radial_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialOffset")

        if temp is None:
            return 0.0

        return temp

    @radial_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialOffset", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def rectangular_duct_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RectangularDuctHeight")

        if temp is None:
            return 0.0

        return temp

    @rectangular_duct_height.setter
    @exception_bridge
    @enforce_parameter_types
    def rectangular_duct_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RectangularDuctHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rectangular_duct_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RectangularDuctWidth")

        if temp is None:
            return 0.0

        return temp

    @rectangular_duct_width.setter
    @exception_bridge
    @enforce_parameter_types
    def rectangular_duct_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RectangularDuctWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rotation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Rotation")

        if temp is None:
            return 0.0

        return temp

    @rotation.setter
    @exception_bridge
    @enforce_parameter_types
    def rotation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Rotation", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def shape(self: "Self") -> "_1380.CoolingDuctShape":
        """mastapy.electric_machines.CoolingDuctShape"""
        temp = pythonnet_property_get(self.wrapped, "Shape")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.CoolingDuctShape"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1380", "CoolingDuctShape"
        )(value)

    @shape.setter
    @exception_bridge
    @enforce_parameter_types
    def shape(self: "Self", value: "_1380.CoolingDuctShape") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.CoolingDuctShape"
        )
        pythonnet_property_set(self.wrapped, "Shape", value)

    @property
    @exception_bridge
    def upper_arc_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UpperArcLength")

        if temp is None:
            return 0.0

        return temp

    @upper_arc_length.setter
    @exception_bridge
    @enforce_parameter_types
    def upper_arc_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "UpperArcLength", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def upper_fillet_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UpperFilletRadius")

        if temp is None:
            return 0.0

        return temp

    @upper_fillet_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def upper_fillet_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UpperFilletRadius",
            float(value) if value is not None else 0.0,
        )

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
    def cast_to(self: "Self") -> "_Cast_CoolingDuctLayerSpecification":
        """Cast to another type.

        Returns:
            _Cast_CoolingDuctLayerSpecification
        """
        return _Cast_CoolingDuctLayerSpecification(self)
