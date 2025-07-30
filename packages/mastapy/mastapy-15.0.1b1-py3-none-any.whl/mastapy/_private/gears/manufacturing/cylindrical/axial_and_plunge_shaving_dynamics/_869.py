"""ShavingDynamicsCalculation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item, overridable
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_SHAVING_DYNAMICS_CALCULATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "ShavingDynamicsCalculation",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.gear_designs.cylindrical import _1135
    from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
        _855,
        _856,
        _861,
        _862,
        _864,
        _865,
        _868,
        _870,
        _871,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _835
    from mastapy._private.gears.manufacturing.cylindrical.cutters import _818

    Self = TypeVar("Self", bound="ShavingDynamicsCalculation")
    CastSelf = TypeVar(
        "CastSelf", bound="ShavingDynamicsCalculation._Cast_ShavingDynamicsCalculation"
    )

T = TypeVar("T", bound="_868.ShavingDynamics")

__docformat__ = "restructuredtext en"
__all__ = ("ShavingDynamicsCalculation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShavingDynamicsCalculation:
    """Special nested class for casting ShavingDynamicsCalculation to subclasses."""

    __parent__: "ShavingDynamicsCalculation"

    @property
    def conventional_shaving_dynamics_calculation_for_designed_gears(
        self: "CastSelf",
    ) -> "_855.ConventionalShavingDynamicsCalculationForDesignedGears":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _855,
        )

        return self.__parent__._cast(
            _855.ConventionalShavingDynamicsCalculationForDesignedGears
        )

    @property
    def conventional_shaving_dynamics_calculation_for_hobbed_gears(
        self: "CastSelf",
    ) -> "_856.ConventionalShavingDynamicsCalculationForHobbedGears":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _856,
        )

        return self.__parent__._cast(
            _856.ConventionalShavingDynamicsCalculationForHobbedGears
        )

    @property
    def plunge_shaving_dynamics_calculation_for_designed_gears(
        self: "CastSelf",
    ) -> "_861.PlungeShavingDynamicsCalculationForDesignedGears":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _861,
        )

        return self.__parent__._cast(
            _861.PlungeShavingDynamicsCalculationForDesignedGears
        )

    @property
    def plunge_shaving_dynamics_calculation_for_hobbed_gears(
        self: "CastSelf",
    ) -> "_862.PlungeShavingDynamicsCalculationForHobbedGears":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _862,
        )

        return self.__parent__._cast(
            _862.PlungeShavingDynamicsCalculationForHobbedGears
        )

    @property
    def shaving_dynamics_calculation_for_designed_gears(
        self: "CastSelf",
    ) -> "_870.ShavingDynamicsCalculationForDesignedGears":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _870,
        )

        return self.__parent__._cast(_870.ShavingDynamicsCalculationForDesignedGears)

    @property
    def shaving_dynamics_calculation_for_hobbed_gears(
        self: "CastSelf",
    ) -> "_871.ShavingDynamicsCalculationForHobbedGears":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _871,
        )

        return self.__parent__._cast(_871.ShavingDynamicsCalculationForHobbedGears)

    @property
    def shaving_dynamics_calculation(self: "CastSelf") -> "ShavingDynamicsCalculation":
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
class ShavingDynamicsCalculation(_0.APIBase, Generic[T]):
    """ShavingDynamicsCalculation

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _SHAVING_DYNAMICS_CALCULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def adjusted_tip_diameter(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustedTipDiameter")

        if temp is None:
            return None

        value = conversion.to_list_any(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def life_cutter_normal_thickness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LifeCutterNormalThickness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @life_cutter_normal_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def life_cutter_normal_thickness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LifeCutterNormalThickness", value)

    @property
    @exception_bridge
    def life_cutter_tip_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LifeCutterTipDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @life_cutter_tip_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def life_cutter_tip_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LifeCutterTipDiameter", value)

    @property
    @exception_bridge
    def new_cutter_tip_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NewCutterTipDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def normal_tooth_thickness_reduction_between_redressings(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NormalToothThicknessReductionBetweenRedressings"
        )

        if temp is None:
            return 0.0

        return temp

    @normal_tooth_thickness_reduction_between_redressings.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_tooth_thickness_reduction_between_redressings(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalToothThicknessReductionBetweenRedressings",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def selected_redressing(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_T":
        """ListWithSelectedItem[T]"""
        temp = pythonnet_property_get(self.wrapped, "SelectedRedressing")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_T",
        )(temp)

    @selected_redressing.setter
    @exception_bridge
    @enforce_parameter_types
    def selected_redressing(self: "Self", value: "T") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_T.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "SelectedRedressing", value)

    @property
    @exception_bridge
    def accuracy_level_iso6(self: "Self") -> "_865.RollAngleRangeRelativeToAccuracy":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.RollAngleRangeRelativeToAccuracy

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AccuracyLevelISO6")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def accuracy_level_iso7(self: "Self") -> "_865.RollAngleRangeRelativeToAccuracy":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.RollAngleRangeRelativeToAccuracy

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AccuracyLevelISO7")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def designed_gear(self: "Self") -> "_835.CylindricalCutterSimulatableGear":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.CylindricalCutterSimulatableGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignedGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def life_cutter_start_of_shaving(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LifeCutterStartOfShaving")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def life_shaver(self: "Self") -> "_818.CylindricalGearShaver":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaver

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LifeShaver")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def new_cutter_start_of_shaving(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NewCutterStartOfShaving")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaver(self: "Self") -> "_818.CylindricalGearShaver":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaver

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shaver")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def redressing_settings(self: "Self") -> "List[_864.RedressingSettings[T]]":
        """List[mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.RedressingSettings[T]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RedressingSettings")

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
    def cutter_simulation_calculation_required(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CutterSimulationCalculationRequired")

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
    def cast_to(self: "Self") -> "_Cast_ShavingDynamicsCalculation":
        """Cast to another type.

        Returns:
            _Cast_ShavingDynamicsCalculation
        """
        return _Cast_ShavingDynamicsCalculation(self)
