"""MicroGeometryViewingOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item_and_image,
)
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1225
from mastapy._private.gears.ltca import _930
from mastapy._private.nodal_analysis import _93

_MICRO_GEOMETRY_VIEWING_OPTIONS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "MicroGeometryViewingOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="MicroGeometryViewingOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicroGeometryViewingOptions._Cast_MicroGeometryViewingOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryViewingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicroGeometryViewingOptions:
    """Special nested class for casting MicroGeometryViewingOptions to subclasses."""

    __parent__: "MicroGeometryViewingOptions"

    @property
    def micro_geometry_viewing_options(
        self: "CastSelf",
    ) -> "MicroGeometryViewingOptions":
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
class MicroGeometryViewingOptions(_0.APIBase):
    """MicroGeometryViewingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICRO_GEOMETRY_VIEWING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_results(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ContactResultType":
        """EnumWithSelectedValue[mastapy.gears.ltca.ContactResultType]"""
        temp = pythonnet_property_get(self.wrapped, "ContactResults")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ContactResultType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @contact_results.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_results(self: "Self", value: "_930.ContactResultType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ContactResultType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ContactResults", value)

    @property
    @exception_bridge
    def gear_option(self: "Self") -> "_1225.DrawDefiningGearOrBoth":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.DrawDefiningGearOrBoth"""
        temp = pythonnet_property_get(self.wrapped, "GearOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry.DrawDefiningGearOrBoth",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1225",
            "DrawDefiningGearOrBoth",
        )(value)

    @gear_option.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_option(self: "Self", value: "_1225.DrawDefiningGearOrBoth") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry.DrawDefiningGearOrBoth",
        )
        pythonnet_property_set(self.wrapped, "GearOption", value)

    @property
    @exception_bridge
    def root_stress_results_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_StressResultsType":
        """EnumWithSelectedValue[mastapy.nodal_analysis.StressResultsType]"""
        temp = pythonnet_property_get(self.wrapped, "RootStressResultsType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_StressResultsType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @root_stress_results_type.setter
    @exception_bridge
    @enforce_parameter_types
    def root_stress_results_type(self: "Self", value: "_93.StressResultsType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StressResultsType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "RootStressResultsType", value)

    @property
    @exception_bridge
    def show_contact_chart(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowContactChart")

        if temp is None:
            return False

        return temp

    @show_contact_chart.setter
    @exception_bridge
    @enforce_parameter_types
    def show_contact_chart(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowContactChart",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_contact_points(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowContactPoints")

        if temp is None:
            return False

        return temp

    @show_contact_points.setter
    @exception_bridge
    @enforce_parameter_types
    def show_contact_points(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowContactPoints",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_force_arrows(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowForceArrows")

        if temp is None:
            return False

        return temp

    @show_force_arrows.setter
    @exception_bridge
    @enforce_parameter_types
    def show_force_arrows(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowForceArrows", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def show_gear(
        self: "Self",
    ) -> "list_with_selected_item_and_image.ListWithSelectedItemAndImage_DrawDefiningGearOrBoth":
        """ListWithSelectedItemAndImage[mastapy.gears.gear_designs.cylindrical.micro_geometry.DrawDefiningGearOrBoth]"""
        temp = pythonnet_property_get(self.wrapped, "ShowGear")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_DrawDefiningGearOrBoth.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @show_gear.setter
    @exception_bridge
    @enforce_parameter_types
    def show_gear(self: "Self", value: "_1225.DrawDefiningGearOrBoth") -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_DrawDefiningGearOrBoth.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ShowGear", value)

    @property
    @exception_bridge
    def show_root_stress_chart(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowRootStressChart")

        if temp is None:
            return False

        return temp

    @show_root_stress_chart.setter
    @exception_bridge
    @enforce_parameter_types
    def show_root_stress_chart(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowRootStressChart",
            bool(value) if value is not None else False,
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
    def cast_to(self: "Self") -> "_Cast_MicroGeometryViewingOptions":
        """Cast to another type.

        Returns:
            _Cast_MicroGeometryViewingOptions
        """
        return _Cast_MicroGeometryViewingOptions(self)
