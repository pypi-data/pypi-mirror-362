"""OilLevelSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2674
from mastapy._private.system_model.part_model.gears import _2762

_OIL_LEVEL_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "OilLevelSpecification"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="OilLevelSpecification")
    CastSelf = TypeVar(
        "CastSelf", bound="OilLevelSpecification._Cast_OilLevelSpecification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("OilLevelSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OilLevelSpecification:
    """Special nested class for casting OilLevelSpecification to subclasses."""

    __parent__: "OilLevelSpecification"

    @property
    def oil_level_specification(self: "CastSelf") -> "OilLevelSpecification":
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
class OilLevelSpecification(_0.APIBase):
    """OilLevelSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OIL_LEVEL_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_for_oil_level_reference(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_CylindricalGear":
        """ListWithSelectedItem[mastapy.system_model.part_model.gears.CylindricalGear]"""
        temp = pythonnet_property_get(self.wrapped, "GearForOilLevelReference")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_CylindricalGear",
        )(temp)

    @gear_for_oil_level_reference.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_for_oil_level_reference(
        self: "Self", value: "_2762.CylindricalGear"
    ) -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_CylindricalGear.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "GearForOilLevelReference", value)

    @property
    @exception_bridge
    def oil_level(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OilLevel")

        if temp is None:
            return 0.0

        return temp

    @oil_level.setter
    @exception_bridge
    @enforce_parameter_types
    def oil_level(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OilLevel", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def oil_level_reference_datum(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Datum":
        """ListWithSelectedItem[mastapy.system_model.part_model.Datum]"""
        temp = pythonnet_property_get(self.wrapped, "OilLevelReferenceDatum")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Datum",
        )(temp)

    @oil_level_reference_datum.setter
    @exception_bridge
    @enforce_parameter_types
    def oil_level_reference_datum(self: "Self", value: "_2674.Datum") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "OilLevelReferenceDatum", value)

    @property
    @exception_bridge
    def oil_level_specified(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OilLevelSpecified")

        if temp is None:
            return False

        return temp

    @oil_level_specified.setter
    @exception_bridge
    @enforce_parameter_types
    def oil_level_specified(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OilLevelSpecified",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_gear_tip_diameter_for_oil_level_reference(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseGearTipDiameterForOilLevelReference"
        )

        if temp is None:
            return False

        return temp

    @use_gear_tip_diameter_for_oil_level_reference.setter
    @exception_bridge
    @enforce_parameter_types
    def use_gear_tip_diameter_for_oil_level_reference(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseGearTipDiameterForOilLevelReference",
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
    def cast_to(self: "Self") -> "_Cast_OilLevelSpecification":
        """Cast to another type.

        Returns:
            _Cast_OilLevelSpecification
        """
        return _Cast_OilLevelSpecification(self)
