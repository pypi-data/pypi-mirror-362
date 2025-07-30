"""PlasticSNCurve"""

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

_PLASTIC_SN_CURVE = python_net_import("SMT.MastaAPI.Gears.Materials", "PlasticSNCurve")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.materials import _705
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _586
    from mastapy._private.materials import _374, _375, _378

    Self = TypeVar("Self", bound="PlasticSNCurve")
    CastSelf = TypeVar("CastSelf", bound="PlasticSNCurve._Cast_PlasticSNCurve")


__docformat__ = "restructuredtext en"
__all__ = ("PlasticSNCurve",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlasticSNCurve:
    """Special nested class for casting PlasticSNCurve to subclasses."""

    __parent__: "PlasticSNCurve"

    @property
    def plastic_sn_curve_for_the_specified_operating_conditions(
        self: "CastSelf",
    ) -> "_586.PlasticSNCurveForTheSpecifiedOperatingConditions":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _586

        return self.__parent__._cast(
            _586.PlasticSNCurveForTheSpecifiedOperatingConditions
        )

    @property
    def plastic_sn_curve(self: "CastSelf") -> "PlasticSNCurve":
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
class PlasticSNCurve(_0.APIBase):
    """PlasticSNCurve

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLASTIC_SN_CURVE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_stress_number_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableStressNumberBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_stress_number_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableStressNumberContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def flank_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FlankTemperature")

        if temp is None:
            return 0.0

        return temp

    @flank_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def flank_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FlankTemperature", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def life_cycles(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LifeCycles")

        if temp is None:
            return 0.0

        return temp

    @life_cycles.setter
    @exception_bridge
    @enforce_parameter_types
    def life_cycles(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LifeCycles", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def lubricant(self: "Self") -> "_378.VDI2736LubricantType":
        """mastapy.materials.VDI2736LubricantType"""
        temp = pythonnet_property_get(self.wrapped, "Lubricant")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.VDI2736LubricantType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._378", "VDI2736LubricantType"
        )(value)

    @lubricant.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant(self: "Self", value: "_378.VDI2736LubricantType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.VDI2736LubricantType"
        )
        pythonnet_property_set(self.wrapped, "Lubricant", value)

    @property
    @exception_bridge
    def nominal_stress_number_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalStressNumberBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def note_1(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Note1")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def note_2(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Note2")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def number_of_rows_in_the_bending_sn_table(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfRowsInTheBendingSNTable")

        if temp is None:
            return 0

        return temp

    @number_of_rows_in_the_bending_sn_table.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_rows_in_the_bending_sn_table(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfRowsInTheBendingSNTable",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_rows_in_the_contact_sn_table(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfRowsInTheContactSNTable")

        if temp is None:
            return 0

        return temp

    @number_of_rows_in_the_contact_sn_table.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_rows_in_the_contact_sn_table(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfRowsInTheContactSNTable",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def root_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RootTemperature")

        if temp is None:
            return 0.0

        return temp

    @root_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def root_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RootTemperature", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def material(self: "Self") -> "_705.PlasticCylindricalGearMaterial":
        """mastapy.gears.materials.PlasticCylindricalGearMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Material")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bending_stress_cycle_data_for_damage_tables(
        self: "Self",
    ) -> "List[_374.StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]":
        """List[mastapy.materials.StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BendingStressCycleDataForDamageTables"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def bending_stress_cycle_data(
        self: "Self",
    ) -> "List[_374.StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]":
        """List[mastapy.materials.StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingStressCycleData")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_stress_cycle_data_for_damage_tables(
        self: "Self",
    ) -> "List[_375.StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]":
        """List[mastapy.materials.StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactStressCycleDataForDamageTables"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_stress_cycle_data(
        self: "Self",
    ) -> "List[_375.StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]":
        """List[mastapy.materials.StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactStressCycleData")

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
    def cast_to(self: "Self") -> "_Cast_PlasticSNCurve":
        """Cast to another type.

        Returns:
            _Cast_PlasticSNCurve
        """
        return _Cast_PlasticSNCurve(self)
