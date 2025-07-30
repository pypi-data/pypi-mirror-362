"""Customer102DataSheetTolerances"""

from __future__ import annotations

from enum import Enum
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

_CUSTOMER_102_DATA_SHEET_TOLERANCES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "Customer102DataSheetTolerances"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.gear_designs.cylindrical import _1115
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1254,
        _1257,
        _1258,
    )

    Self = TypeVar("Self", bound="Customer102DataSheetTolerances")
    CastSelf = TypeVar(
        "CastSelf",
        bound="Customer102DataSheetTolerances._Cast_Customer102DataSheetTolerances",
    )


__docformat__ = "restructuredtext en"
__all__ = ("Customer102DataSheetTolerances",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Customer102DataSheetTolerances:
    """Special nested class for casting Customer102DataSheetTolerances to subclasses."""

    __parent__: "Customer102DataSheetTolerances"

    @property
    def customer_102_data_sheet_tolerances(
        self: "CastSelf",
    ) -> "Customer102DataSheetTolerances":
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
class Customer102DataSheetTolerances(_0.APIBase):
    """Customer102DataSheetTolerances

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOMER_102_DATA_SHEET_TOLERANCES

    class EatonManufacturingOptionsEnum(Enum):
        """EatonManufacturingOptionsEnum is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _CUSTOMER_102_DATA_SHEET_TOLERANCES.EatonManufacturingOptionsEnum

        SHAVED = 0
        FLANK_AND_FULL_FILLET_GROUND_CBN = 1
        FLANK_ONLY_GROUND_CBN = 2
        FLANK_ONLY_GROUND_VITREOUS_WHEEL = 3
        FLANK_ONLY_FINE_HONE = 4
        FINISH_HOBSHAPERBROACH = 5

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    EatonManufacturingOptionsEnum.__setattr__ = __enum_setattr
    EatonManufacturingOptionsEnum.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def crowning_tolerance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CrowningTolerance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @crowning_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def crowning_tolerance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CrowningTolerance", value)

    @property
    @exception_bridge
    def customer_102_manufacturing_options(
        self: "Self",
    ) -> "Customer102DataSheetTolerances.EatonManufacturingOptionsEnum":
        """mastapy.gears.gear_designs.cylindrical.Customer102DataSheetTolerances.EatonManufacturingOptionsEnum"""
        temp = pythonnet_property_get(self.wrapped, "Customer102ManufacturingOptions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.Customer102DataSheetTolerances+EatonManufacturingOptionsEnum",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical.Customer102DataSheetTolerances.Customer102DataSheetTolerances",
            "EatonManufacturingOptionsEnum",
        )(value)

    @customer_102_manufacturing_options.setter
    @exception_bridge
    @enforce_parameter_types
    def customer_102_manufacturing_options(
        self: "Self",
        value: "Customer102DataSheetTolerances.EatonManufacturingOptionsEnum",
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.Customer102DataSheetTolerances+EatonManufacturingOptionsEnum",
        )
        pythonnet_property_set(self.wrapped, "Customer102ManufacturingOptions", value)

    @property
    @exception_bridge
    def high_point_max(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "HighPointMax")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @high_point_max.setter
    @exception_bridge
    @enforce_parameter_types
    def high_point_max(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "HighPointMax", value)

    @property
    @exception_bridge
    def high_point_min(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "HighPointMin")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @high_point_min.setter
    @exception_bridge
    @enforce_parameter_types
    def high_point_min(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "HighPointMin", value)

    @property
    @exception_bridge
    def involute_variation(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InvoluteVariation")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @involute_variation.setter
    @exception_bridge
    @enforce_parameter_types
    def involute_variation(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InvoluteVariation", value)

    @property
    @exception_bridge
    def lead_range(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadRange")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lead_variation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadVariation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_range(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchRange")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def quality_number_lead(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "QualityNumberLead")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @quality_number_lead.setter
    @exception_bridge
    @enforce_parameter_types
    def quality_number_lead(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "QualityNumberLead", value)

    @property
    @exception_bridge
    def quality_number_runout(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "QualityNumberRunout")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @quality_number_runout.setter
    @exception_bridge
    @enforce_parameter_types
    def quality_number_runout(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "QualityNumberRunout", value)

    @property
    @exception_bridge
    def quality_number_tooth_tooth(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "QualityNumberToothTooth")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @quality_number_tooth_tooth.setter
    @exception_bridge
    @enforce_parameter_types
    def quality_number_tooth_tooth(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "QualityNumberToothTooth", value)

    @property
    @exception_bridge
    def specify_upper_and_lower_limits_separately(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "SpecifyUpperAndLowerLimitsSeparately"
        )

        if temp is None:
            return False

        return temp

    @specify_upper_and_lower_limits_separately.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_upper_and_lower_limits_separately(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyUpperAndLowerLimitsSeparately",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_mast_as_accuracy_grades(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseMASTAsAccuracyGrades")

        if temp is None:
            return False

        return temp

    @use_mast_as_accuracy_grades.setter
    @exception_bridge
    @enforce_parameter_types
    def use_mast_as_accuracy_grades(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseMASTAsAccuracyGrades",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def accuracy_grades_specified_accuracy(
        self: "Self",
    ) -> "_1257.CylindricalAccuracyGrades":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.CylindricalAccuracyGrades

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AccuracyGradesSpecifiedAccuracy")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def customer_102agma2000_accuracy_grader(
        self: "Self",
    ) -> "_1254.Customer102AGMA2000AccuracyGrader":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.Customer102AGMA2000AccuracyGrader

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Customer102AGMA2000AccuracyGrader")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_accuracy_tolerances(
        self: "Self",
    ) -> "_1258.CylindricalGearAccuracyTolerances":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.CylindricalGearAccuracyTolerances

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearAccuracyTolerances")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def customer_102_tolerance_definitions(
        self: "Self",
    ) -> "List[_1115.Customer102ToleranceDefinition]":
        """List[mastapy.gears.gear_designs.cylindrical.Customer102ToleranceDefinition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Customer102ToleranceDefinitions")

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
    def cast_to(self: "Self") -> "_Cast_Customer102DataSheetTolerances":
        """Cast to another type.

        Returns:
            _Cast_Customer102DataSheetTolerances
        """
        return _Cast_Customer102DataSheetTolerances(self)
